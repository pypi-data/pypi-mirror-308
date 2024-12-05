#!/bin/bash -e

rustup update
export CARGO_HOME=/event_voxel_builder/cargo_home/
export PYO3_PYTHON=${PYTHON}
git config --global --add safe.directory /event_voxel_builder
cargo clean
cargo update
cargo build --release
${PYTHON} -m maturin build --release
unalias cp
unalias rm
rm -rf release/
mkdir release/
cp target/wheels/event_voxel_builder-*.whl release/
cp -r examples/ release/
cd release/
find ./ -name "__pycache__" -o -name "*.pyc" | xargs rm -rf
rm -r examples/scripts_*
tar -czf ../event_voxel_builder_linux.tar.gz *
