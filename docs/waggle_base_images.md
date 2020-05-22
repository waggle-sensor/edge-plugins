### Waggle Base Docker Images

Last updated: 05/22/2020

User applications that will run on Waggle nodes must be containerized as Waggle utilizes a container management tool to deploy user applications to the Waggle nodes. Because user applications vary in required software libraries and tools Waggle presents a set of Docker images to help the needs. Some of the Waggle Docker images support Nvidia's CUDA graphics cards to enable GPU acceleration for machine learning applications. 

#### Cheat-sheet Table for Docker Images

The table below shows the available Waggle Docker images as of now. 

NOTE: All the images support x86_64, arm64, and armv7 platforms. 

NOTE: The Waggle Docker images listed below are based on their version of `0.1.0`

| Image name | base | software | ML tools | etc |
|---|---|---|---|---|
| [waggle-base](https://hub.docker.com/r/waggle/plugin-base) | Ubuntu18.04 | Python3.6,Numpy1.17.4,git,nano | N/A |   |
| [waggle-base-light](https://hub.docker.com/r/waggle/plugin-base-light) | Alpine 3.10.2 | Python3.7,Numpy1.16,git,nano | N/A |   |
| [waggle-base-gpu](https://hub.docker.com/r/waggle/plugin-base-gpu) | Ubuntu18.04 | Python3.6,Numpy1.17.4,git,nano | CUDA 10.1(for arm64)/10.2(for x86_64),Mali T-62x  |   |
| [waggle-opencv](https://hub.docker.com/r/waggle/plugin-opencv) | waggle-base-gpu | codecs,image libraries  | OpenCV 4.1.1 |   |
| [waggle-tensorflow](https://hub.docker.com/r/waggle/plugin-tensorflow) | waggle-base-gpu | hdf5,atlas | TensorFlow 1.4 / 2.1.0  |   |
| [waggle-torch](https://hub.docker.com/r/waggle/plugin-torch) | waggle-base-gpu | N/A  | PyTorch 1.4.0,Torchvision 0.5.0  |   |
| [waggle-training-fcn](https://hub.docker.com/r/waggle/plugin-training-fcn) | waggle-torch | N/A  | FCN models  |   |
| [waggle-training-yolov3](https://hub.docker.com/r/waggle/plugin-training-yolov3) | waggle-torch | Pillow | YoloV3 model,tensorboardx  |   |

#### Supported Hardware

The current set of Waggle Docker images support any x86_64 based system, any armv7l based system (without GPU acceleration), and Nvidia Jetson family devices (i.e., Nano, TX2, and more). We plan to support [Coral Dev board](https://coral.ai/products/dev-board), [Coral USB Accelerator](https://coral.ai/products/accelerator), and [Intel Neural Compute Stick](https://software.intel.com/content/www/us/en/develop/hardware/neural-compute-stick.html).

#### Waggle Base Images

Base images simply provides the base for plugins to be running. There are 3 types of base imabes,

1) `waggle-base`: Ubuntu 18.04 based image; suitable for any edge plugin that do not require GPU acceleration
2) `waggle-base-light`: Alpine 3.10.X based image; suitable for edge plugins that do not require heavy computation
3) `waggle-base-gpu`: Ubuntu 18.04 based image with GPU libraries; suitable for edge plugins that need GPU acceleration

#### Waggle Images for Machine Learning

Common machine learning tools such as TensorFlow, OpenCV, PyTorch are supported by Waggle images. The ML Waggle images are based on `plugin-base-gpu` for GPU acceleration on the ML tools.

1) `waggle-opencv`: OpenCV 4.1.1 with contribution packages are supported
2) `waggle-tensorflow`: TensorFlow 1.4.0 and 2.0.0 (in progress) are supported
3) `waggle-torch`: Torch 1.4.0 and Torchvision 0.5.0 (Pillow 6.2.1) are supported

#### Waggle Images for Cloud Training

A few Waggle images support cloud training capability.

__NOTE: This is primarily under development__

1) `waggle-training-fcn`: Image segmentation using fully connected network (FCN) with Resnet and VGG16 base networks
2) `waggle-training-yolov3`: Object detection using Yolov3 network
