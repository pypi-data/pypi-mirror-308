#!/bin/bash -e

rustup update
export CARGO_HOME=/event_voxel_builder/cargo_home/
export PYO3_PYTHON=${PYTHON}
git config --global --add safe.directory /event_voxel_builder
source ./examples/scripts_unix/build/credentials.sh
cargo clean
cargo update
cargo login $CARGO_TOKEN
cargo publish --no-verify || true
${PYTHON} -m maturin publish --non-interactive || true
cargo doc --no-deps --document-private-items
rm -rf pages/
mkdir pages/
cd pages/
git config --global --add safe.directory /event_voxel_builder/pages
git init -b pages
echo "* text eol=lf" > .gitattributes
echo ".lock" > .gitignore
echo "<meta http-equiv=\"refresh\" content=\"0; url=event_voxel_builder\">" > index.html
cp -r ../target/doc/* ./
git add .
git commit -m "Update pages"
git remote add origin $GIT_REPO
git push --set-upstream origin --force pages
cd ../
rm -rf pages/
