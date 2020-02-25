### Training Resnet101-FCN network

The docker file is providing a method of training a semantic segmentation model, Resnet101 based FCN network, using PyTorch 1.3.
Basically, python3 libraries; torch, torchvision, tqdm, fcn, and fcn related libraries are necessary.
The code is supporting CPU and CUDA.

For any of image pairs of original images and labeled images can use this method for segmentation.
An example usage of this method is cloud coverage estimation.

### How train:

python3 test_trainig.py

### Adjustment required:

The code is based on a FCN model that provided by PyTorch so that it is always trying to download the base model from PyTorch server.
Therefore, the base model need to be added in the package and the path for the base model needs to be re-identified.

Most of the parameters are hard-coded; especially the input path for both folders for raw images and labeled images.
This issue also needs to be re-designed.
