// Document need to be synced with `README.md` manually.
//! # Fast Event Voxel Builder
//! [\[Codeberg Repo\]](https://codeberg.org/ybh1998/EventVoxelBuilder/)
//! [\[API Document\]](https://ybh1998.codeberg.page/EventVoxelBuilder/)
//!
//! ### Warning: Very Unstable API!
//! This is currently a rush project for CVPR 2024 and the API will definitely be rewritten after the DDL.
//!
//! ### To run the example Python codes or your own Python code
//! 1. Download `event-voxel-builder-*.whl` under
//! [\[releases\]](https://codeberg.org/ybh1998/EventVoxelBuilder/releases/) and install using `pip install`, or
//! install from [\[PyPI\]](https://pypi.org/project/event-voxel-builder/).
//! 2. Run Python example codes in `examples` or your own codes.
//!
//! Copyright (c) 2023 Bohan Yu. All rights reserved. \
//! EventVoxelBuilder is free software licensed under GNU Affero General Public License version 3 or latter.

use std::env;
use anyhow::Result;
use pyo3::prelude::*;
use shadow_rs::shadow;
use tracing_subscriber::{fmt, EnvFilter, prelude::*};
use self::event_simulator::PyEventSimulator;
use self::event_voxel_builder::PyEventVoxelBuilder;

mod event_simulator;
mod event_voxel_builder;

shadow!(build);



fn init_static() -> Result<()> {
  let log_level = env::var("EVENT_VOXEL_BUILDER_LOG_LEVEL").unwrap_or(String::from("info"));
  let filter_layer = EnvFilter::try_new(log_level)?;
  let fmt_layer = fmt::layer()
    .with_target(false);
  tracing_subscriber::registry()
    .with(filter_layer)
    .with(fmt_layer)
    .init();
  Ok(())
}

/// Initialize Python module.
///
/// Accept `EVENT_VOXEL_BUILDER_LOG_LEVEL` environment variable to set `log_level`.
/// * (default: info, feasible: debug, info, warn, error)
#[pymodule]
#[pyo3(name = "event_voxel_builder")]
pub fn py_event_voxel_builder(module: &Bound<'_, PyModule>) -> PyResult<()> {
  init_static()?;
  module.add("__author__", "Bohan Yu <ybh1998@protonmail.com>")?;
  module.add("__version__", format!("EventVoxelBuilder {}", build::PKG_VERSION))?;
  module.add_class::<PyEventSimulator>()?;
  module.add_class::<PyEventVoxelBuilder>()?;
  Ok(())
}
