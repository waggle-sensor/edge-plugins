### Inference Cloud Coverage using Resnet101-FCN network on PyTorch

The docker file is providing a method of inference a semantic segmentation model, Resnet101 based FCN network, using PyTorch 1.3. Basically, python3 libraries; torch, torchvision, tqdm, fcn, and fcn related libraries are necessary. The code is supporting CPU or CUDA based on how the model that is loaded on was trained.

For any of image can use this method for segmentation. An example usage of this method is cloud coverage estimation and water flooding/ponding detection.

### How to use:

python3 run.py input_path

### Adjustment required:

- The code is based on a FCN model that provided by PyTorch so that it is always trying to download the base model from PyTorch server. Therefore, the base model need to be added in the package and the path for the base model needs to be re-identified.

- The path of the model in the code is hard coded, so it would be better to re-design the part.
