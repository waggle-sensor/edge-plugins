### Downloading CUDA 10 and CuDNN 7 for Tegra Linux

As of December 2019, Nvidia does not provide direct link to the CUDA 10 and CuDNN 7 packages for Tegra Linux. The two packages however can be downloaded via [SDK Manager](https://developer.nvidia.com/nvidia-sdk-manager). Downloading and using SDK Manager requires a Nvidia developer membership. Once the two packages are downloaded using SDK Manager, copy the packages from `$(HOME)/Downloads/nvidia/sdkm_downloads/` to the directory to which Docker context points (by default the directory where the Dockerfiles located).

As of December 2019, the CUDA and CuDNN packages for Tegra Linux only exist in developer version. The CUDA and CuDNN for amd86 architecture support both developer and runtime version.

### CUDA Driver Library in Docker Container

`nvidia/cuda` Docker image does not contain CUDA driver, *libcuda.so*. When a Docker container from the image is created with `--runtime nvidia`, the driver is put inside the container under `/usr/lib/x86_64-linux-gnu`. The symbolic link below in the Dockerfile.cuda helps users find the CUDA driver easily.

```
ln -sf /usr/lib/x86_64-linux-gnu/libcuda.so /usr/local/lib/libcuda.so.1
```