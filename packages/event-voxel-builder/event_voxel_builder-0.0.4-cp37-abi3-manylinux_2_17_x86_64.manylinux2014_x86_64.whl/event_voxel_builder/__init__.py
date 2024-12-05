import numpy as np
# Rust modules
from .event_voxel_builder import __author__, __version__
from .event_voxel_builder import EventSimulator as RustEventSimulator
from .event_voxel_builder import EventVoxelBuilder as RustEventVoxelBuilder

class EventSimulator(RustEventSimulator):
  def add_frame(self, frame, time):
    if len(frame.shape) == 2:
      frame = np.repeat(frame[..., None], 3, -1)
    return super().add_frame(frame, time)

class EventVoxelBuilder(RustEventVoxelBuilder):
  def build(self, timestamps, i_row, i_col, polarity):
    timestamps = np.ascontiguousarray(timestamps, dtype=np.uint64)
    i_row = np.ascontiguousarray(i_row, dtype=np.uint16)
    i_col = np.ascontiguousarray(i_col, dtype=np.uint16)
    polarity = np.ascontiguousarray(polarity, dtype=np.int8)
    return super().build(timestamps, i_row, i_col, polarity)
