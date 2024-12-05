# Compatible with CentOS based image
FROM quay.io/pypa/manylinux2014_x86_64

# Python version need to be updated along with pyo3 minimum requirement
ARG PYTHON

# Install dependencies
RUN yum install -y git && yum clean all

# Install rust toolchain using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Install maturin to build python wheels
ENV PYTHON=${PYTHON}
RUN ${PYTHON} -m pip install maturin

# PWD is mounted as volume in build.sh
WORKDIR /event_voxel_builder/
