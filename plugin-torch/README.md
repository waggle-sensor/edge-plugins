### PyTorch for ARMv7

Unlike other popular architecture, ARMv7 is not officially supported from PyTorch community, as of 03/12/2020. The following multistage Dockerfile makes a Docker image with the libraries installed.

__WARNING: if the build is executed under Odroid-XU4 or similar hardware, it may take a couple of days to finish compiling torch library; Also make a sufficient amount of swap memory; 4 GB is recommended on Odroid-xU4__

```
# Dockerfile for Pytorch compile environment
FROM waggle/plugin-base-gpu:0.1.0 as BUILD

ENV torch_ver="v1.4.0"
ENV torchvision_ver="v0.5.0"

RUN apt-get update \
  && apt-get install -y \
  cmake \
  git \
  libssl-dev \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# NOTE: The following RUNs are intentionally divided
#       as Odroid-XU4 with 2 GB swap memory suffers from Out-of-Memory
#       or 4 GB swap memory can be set
RUN pip3 install --no-cache-dir scikit-build
RUN pip3 install --no-cache-dir cmake
RUN pip3 install --no-cache-dir ninja pyyaml cffi

RUN cd /tmp \
  && git clone --recursive https://github.com/pytorch/pytorch \
  && cd /tmp/pytorch \
  && git checkout ${torch_ver} \
  && git submodule sync \
  && git submodule update --init --recursive
  
RUN cd /tmp/pytorch \
  && export USE_CUDA=0 \
  && export USE_MKLDNN=0 \
  && export USE_NNPACK=0 \
  && export USE_QNNPACK=0 \
  && export USE_DISTRIBUTED=0 \
  && python3 setup.py install bdist_wheel

RUN cd /tmp \
  && git clone --recursive https://github.com/pytorch/vision \
  && cd /tmp/vision \
  && git checkout ${torchvision_ver} \
  && python3 setup.py bdist_wheel
  
FROM waggle/plugin-base-gpu:0.1.0

COPY --from BUILD /tmp/torch/dist/* /tmp
COPY --from BUILD /tmp/vision/dist/* /tmp
RUN apt-get update \
  && apt-get install -y \
  libopenblas-base \
  zlib1g-dev \
  libjpeg-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install Cython Pillow==6.2.1

RUN cd /tmp \
  && pip3 install *.whl \
  && rm -rf *.whl
```
