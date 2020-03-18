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

Here is the configuration summary for your reference,

```
-- 
-- ******** Summary ********
-- General:
--   CMake version         : 3.16.3
--   CMake command         : /usr/local/lib/python3.6/dist-packages/cmake/data/bin/cmake
--   System                : Linux
--   C++ compiler          : /usr/bin/c++
--   C++ compiler id       : GNU
--   C++ compiler version  : 7.4.0
--   BLAS                  : MKL
--   CXX flags             :  -Wno-deprecated -fvisibility-inlines-hidden -fopenmp -DUSE_PYTORCH_QNNPACK -O2 -fPIC -Wno-narrowing -Wall -Wextra -Wno-missing-field-initializers -Wno-type-limits -Wno-array-bounds -Wno-unknown-pragmas -Wno-sign-compare -Wno-unused-parameter -Wno-unused-variable -Wno-unused-function -Wno-unused-result -Wno-strict-overflow -Wno-strict-aliasing -Wno-error=deprecated-declarations -Wno-stringop-overflow -Wno-error=pedantic -Wno-error=redundant-decls -Wno-error=old-style-cast -fdiagnostics-color=always -faligned-new -Wno-unused-but-set-variable -Wno-maybe-uninitialized -fno-math-errno -fno-trapping-math -Wno-stringop-overflow
--   Build type            : Release
--   Compile definitions   : ONNX_ML=1;ONNX_NAMESPACE=onnx_torch;HAVE_MMAP=1;_FILE_OFFSET_BITS=64;HAVE_SHM_OPEN=1;HAVE_SHM_UNLINK=1;HAVE_MALLOC_USABLE_SIZE=1
--   CMAKE_PREFIX_PATH     : /usr/lib/python3/dist-packages
--   CMAKE_INSTALL_PREFIX  : /storage/pytorch/torch
-- 
--   TORCH_VERSION         : 1.4.0
--   CAFFE2_VERSION        : 1.4.0
--   BUILD_CAFFE2_MOBILE   : ON
--   USE_STATIC_DISPATCH   : OFF
--   BUILD_BINARY          : OFF
--   BUILD_CUSTOM_PROTOBUF : ON
--     Link local protobuf : ON
--   BUILD_DOCS            : OFF
--   BUILD_PYTHON          : True
--     Python version      : 3.6.9
--     Python executable   : /usr/bin/python3
--     Pythonlibs version  : 3.6.9
--     Python library      : /usr/lib/libpython3.6m.so.1.0
--     Python includes     : /usr/include/python3.6m
--     Python site-packages: lib/python3/dist-packages
--   BUILD_CAFFE2_OPS      : ON
--   BUILD_SHARED_LIBS     : ON
--   BUILD_TEST            : True
--   BUILD_JNI             : OFF
--   INTERN_BUILD_MOBILE   : 
--   USE_ASAN              : OFF
--   USE_CUDA              : 0
--   USE_ROCM              : OFF
--   USE_EIGEN_FOR_BLAS    : ON
--   USE_FBGEMM            : OFF
--   USE_FFMPEG            : OFF
--   USE_GFLAGS            : OFF
--   USE_GLOG              : OFF
--   USE_LEVELDB           : OFF
--   USE_LITE_PROTO        : OFF
--   USE_LMDB              : OFF
--   USE_METAL             : OFF
--   USE_MKL               : OFF
--   USE_MKLDNN            : OFF
--   USE_NCCL              : OFF
--   USE_NNPACK            : 0
--   USE_NUMPY             : ON
--   USE_OBSERVERS         : ON
--   USE_OPENCL            : OFF
--   USE_OPENCV            : OFF
--   USE_OPENMP            : ON
--   USE_TBB               : OFF
--   USE_PROF              : OFF
--   USE_QNNPACK           : 0
--   USE_REDIS             : OFF
--   USE_ROCKSDB           : OFF
--   USE_ZMQ               : OFF
--   USE_DISTRIBUTED       : 0
--   BUILD_NAMEDTENSOR   : OFF
--   Public Dependencies  : Threads::Threads
--   Private Dependencies : pytorch_qnnpack;cpuinfo;fp16;aten_op_header_gen;foxi_loader;rt;gcc_s;gcc;dl
-- Configuring done
-- Generating done
```
