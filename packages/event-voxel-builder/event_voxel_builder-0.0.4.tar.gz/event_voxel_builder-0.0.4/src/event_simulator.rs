use fastrand::Rng;
use pyo3::prelude::*;
use ndarray::prelude::*;
use anyhow::{Result, ensure};
use numpy::{PyReadonlyArray3, PyArray1, ToPyArray};

// const INTENSITY_EPS: f32 = 3. / 255.;
const INTENSITY_EPS: f32 = 1e-3;

fn events_sort_by_time(events: ArrayView2::<f32>) -> Array2::<f32> {
  let mut perm: Vec<usize> = (0..events.nrows()).collect();
  perm.sort_unstable_by(|a, b| events[[*a, 3]].partial_cmp(&events[[*b, 3]]).expect("Internal array"));
  let mut events_sorted = Array2::zeros(events.raw_dim());
  for (mut events_sorted, perm) in events_sorted.outer_iter_mut().zip(perm.into_iter()) {
    events_sorted.assign(&events.row(perm));
  }
  events_sorted
}

#[derive(Clone)]
enum EventStatus {
  Refractory(f32),
  Ready(f32, f32),
}

struct EventConfig {
  event_threshold_mean: f32,
  event_threshold_std: f32,
  event_refractory: f32,
  rng: Rng,
}

impl EventConfig {
  fn sample_threshold(&mut self) -> f32 {
    let threshold = self.event_threshold_mean + (2. * self.rng.f32() - 1.) * f32::sqrt(3.) * self.event_threshold_std;
    f32::max(threshold, 1e-6)
  }
}

pub struct EventSimulator {
  event_status: Array2<EventStatus>,
  last_frame_log: Option<(Array2<f32>, f32)>,
  event_config: EventConfig,
  i_frame: usize,
}

impl EventSimulator {
  pub fn new(
      n_row: u16,
      n_col: u16,
      event_threshold_mean: f32,
      event_threshold_std: Option<f32>,
      event_refractory: Option<f32>,
      seed: Option<u64>) -> Result<Self> {
    ensure!(event_threshold_mean > 0.);
    let event_threshold_std = event_threshold_std.unwrap_or(0.);
    ensure!(event_threshold_std >= 0.);
    let event_refractory = event_refractory.unwrap_or(0.);
    ensure!(event_refractory >= 0.);
    let rng = Rng::with_seed(seed.unwrap_or(0));
    let event_config = EventConfig {
      event_threshold_mean,
      event_threshold_std,
      event_refractory,
      rng,
    };
    Ok(EventSimulator {
      event_status: Array2::from_elem((n_row as usize, n_col as usize), EventStatus::Refractory(event_refractory)),
      last_frame_log: None,
      event_config,
      i_frame: 0,
    })
  }

  pub fn add_frame(
      &mut self,
      frame: ArrayView3<f32>,
      time: f32) -> Result<(Array1<u64>, Array1<u16>, Array1<u16>, Array1<i8>)> {
    ensure!(frame.shape()[0] == self.event_status.shape()[0]);
    ensure!(frame.shape()[1] == self.event_status.shape()[1]);
    ensure!(frame.shape()[2] == 3);
    let frame_log = frame.map_axis(Axis(2), |frame| {
      let gray = frame[0] * 0.114 + frame[1] * 0.587 + frame[2] * 0.299;
      assert!(gray.is_finite(), "{:?}", self.i_frame);
      assert!(gray >= 0., "{:?}", self.i_frame);
      assert!(gray < 1e6, "{:?}", self.i_frame);
      (gray + INTENSITY_EPS).ln()
    });
    let mut events = Array2::zeros((0, 4));
    if let Some((last_frame_log, last_time)) = &self.last_frame_log {
      ensure!(time > last_time);
      for i_row in 0..frame_log.nrows() {
        for i_col in 0..frame_log.ncols() {
          let event_status = &mut self.event_status[(i_row, i_col)];
          let frame_log = &frame_log[(i_row, i_col)];
          let last_frame_log = &last_frame_log[(i_row, i_col)];
          loop {
            *event_status = match event_status {
              EventStatus::Refractory(time_ready) => {
                if *time_ready > time {
                  break;
                }
                let ratio = (*time_ready - last_time) / (time - last_time);
                let baseline = last_frame_log * (1. - ratio) + frame_log * ratio;
                let threshold = self.event_config.sample_threshold();
                EventStatus::Ready(baseline, threshold)
              },
              EventStatus::Ready(baseline, threshold) => {
                if (*baseline - frame_log).abs() < *threshold {
                  break;
                }
                let polarity = (frame_log - *baseline).signum();
                let target = *baseline + polarity * *threshold;
                let ratio = (target - last_frame_log) / (frame_log - last_frame_log);
                let trigger_time = last_time * (1. - ratio) + time * ratio;
                events.push_row(aview1(&[i_row as f32, i_col as f32, polarity, trigger_time])).expect("Internal array");
                EventStatus::Refractory(trigger_time + self.event_config.event_refractory)
              },
            }
          }
        }
      }
    }
    let events = events_sort_by_time(events.view());
    let timestamp = events.map_axis(Axis(1), |v| (v[3] * 1e6) as u64);
    let i_row = events.map_axis(Axis(1), |v| v[0] as u16);
    let i_col = events.map_axis(Axis(1), |v| v[1] as u16);
    let polarity = events.map_axis(Axis(1), |v| v[2] as i8);
    self.last_frame_log = Some((frame_log, time));
    self.i_frame += 1;
    Ok((timestamp, i_row, i_col, polarity))
  }
}

#[pyclass(name = "EventSimulator", subclass)]
pub struct PyEventSimulator {
  event_simulator: EventSimulator,
}

#[pymethods]
impl PyEventSimulator {
  #[new]
  fn py_new(
      n_row: u16,
      n_col: u16,
      event_threshold_mean: f32,
      event_threshold_std: Option<f32>,
      event_refractory: Option<f32>,
      seed: Option<u64>) -> Result<Self> {
    Ok(PyEventSimulator {
      event_simulator: EventSimulator::new(
        n_row,
        n_col,
        event_threshold_mean,
        event_threshold_std,
        event_refractory, seed)?,
    })
  }

  #[pyo3(name = "add_frame")]
  fn py_add_frame<'py>(
      &mut self,
      py: Python<'py>,
      frame: PyReadonlyArray3<f32>,
      time: f32
    ) -> Result<(
      Bound<'py, PyArray1<u64>>,
      Bound<'py, PyArray1<u16>>,
      Bound<'py, PyArray1<u16>>,
      Bound<'py, PyArray1<i8>>)> {
    let frame = frame.as_array();
    let (timestamp, i_row, i_col, polarity) = py.allow_threads(|| {
      self.event_simulator.add_frame(frame, time)
    })?;
    Ok((timestamp.to_pyarray_bound(py), i_row.to_pyarray_bound(py), i_col.to_pyarray_bound(py), polarity.to_pyarray_bound(py)))
  }
}
