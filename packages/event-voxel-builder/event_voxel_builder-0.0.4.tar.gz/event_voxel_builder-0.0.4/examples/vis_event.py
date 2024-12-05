import os
import lzma
import cv2 as cv
import numpy as np
from event_voxel_builder import EventVoxelBuilder

def visualization(voxel_slice, name):
  image = np.clip(voxel_slice * 0.2 + 0.5, 0., 1.)
  image = (image * 255).astype(np.uint8)
  cv.imshow(name, image)
  cv.imwrite(os.path.join(SCRIPT_DIR, name + ".png"), image)

def main(event_path):
  with lzma.open(event_path, "rb") as f:
    events = np.frombuffer(f.read(), dtype=np.float32).reshape(-1, 4)
  for i in range(4):
    print(f"events {i}", events[:, i].min(), events[:, i].max())
  i_row = events[:, 0]
  i_col = events[:, 1]
  polarity = events[:, 2]
  timestamp = (events[:, 3] * 1e6)
  timestamp -= timestamp.min()
  event_voxel_builder = EventVoxelBuilder(n_time=200, n_row=256, n_col=256, timestamp_per_time=1000)
  voxel = event_voxel_builder.build(timestamp, i_row, i_col, polarity)
  print("voxel", voxel.shape, voxel.dtype, voxel.min(), voxel.max())
  visualization(voxel[voxel.shape[0] // 2, :, :], "X-Y")
  visualization(voxel[:, voxel.shape[1] // 2, :], "T-Y")
  visualization(voxel[:, :, voxel.shape[2] // 2], "T-X")
  cv.waitKey(0)
  print("Warning test")
  event_voxel_builder = EventVoxelBuilder(n_time=180, n_row=200, n_col=200, timestamp_per_time=1000)
  voxel = event_voxel_builder.build(timestamp, i_row, i_col, polarity)

if __name__ == "__main__":
  SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
  main(os.path.join(SCRIPT_DIR, "event.xz"))
