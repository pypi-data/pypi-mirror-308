#!/bin/bash -e

# python version need to be updated along with pyo3 minimum requirement
export PYTHON="python3.7"

# You can build the event_voxel_builder_build docker image from Dockerfile:
docker build -t event_voxel_builder_build --build-arg PYTHON=${PYTHON} .
# or download it from quay.io:
# TBD

# project path
export PROJECT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"

docker run -it --rm --volume ${PROJECT_DIR}/:/event_voxel_builder/ event_voxel_builder_build bash -i ./examples/scripts_unix/build/publish_docker.sh
