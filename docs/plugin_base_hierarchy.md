### Plugin Hierarchy

Waggle edge plugins can be packaged from Waggle Docker images. Those base images support commonly used libraries and GPU acceleration libraries.

#### Waggle Base Images

Base images simply provides the base for plugins to be running. There are 3 types of base imabes,

1) `plugin-base`: Ubuntu 18.04 based image; suitable for any edge plugin that do not require GPU acceleration
2) `plugin-base-light`: Alpine 3.10.X based image; suitable for edge plugins that do not require heavy computation
3) `plugin-base-gpu`: Ubuntu 18.04 based image with GPU libraries; suitable for edge plugins that need GPU acceleration

#### Waggle Images for Machine Learning

Common machine learning tools such as TensorFlow, OpenCV, PyTorch are supported by Waggle images. The ML Waggle images are based on `plugin-base-gpu` for GPU acceleration on the ML tools.

1) `plugin-opencv`: OpenCV 4.1.1 with contribution packages are supported
2) `plugin-tensorflow`: TensorFlow 1.4.0 and 2.0.0 (in progress) are supported
3) `plugin-torch`: Torch 1.4.0 and Torchvision 0.5.0 (Pillow 6.2.1) are supported

#### Waggle Images for Cloud Training

A few Waggle images support cloud training capability.

__NOTE: This is primarily under development__

1) `plugin-training-fcn`: Image segmentation using fully connected network (FCN) with Resnet and VGG16 base networks
2) `plugin-training-yolov3`: Object detection using Yolov3 network
