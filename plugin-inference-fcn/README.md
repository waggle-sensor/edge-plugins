### Inference Resnet-FCN network on PyTorch
The plugin inference images using fcn models: resnet101 based fcn101 and fcn50. To run the plugin, the user must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.


1) Preparing Inference Configuration

- `config.list` (or other file name that user named) is a file containing configuration of the inference as shown below; user can modify configuration for their use (The possible pair of backbone and fcn are: `{resnet, 101}, {resnet, 50}:
```
{
    "backbone": "resnet",
    "fcn": "101",
    "output_dir": "output",
    "model": "logs/MODEL-resnet101/model_best.pth.tar",
    "n_classes": "2"
}
```


2) Trained model

The plugin requires a base fcn model with regard to what the user is tyring to inference. The host machine will automatically download the model from PyTorch server. Based on the fcn net, the inference script adds weight from the model that user adds on configuration file, `config.list`.

- `model` in the configuration is a path to a prerained PyTorch model.


**All of the files and folders must be in one folder, and the folder needs to be mounted as `/storage`. The Docker image assumes that the config.list and the trained model are in under `/storage`**


3) Inference

To inference, simply run the command below on the host machine. Please make sure to set all the path correct.


```
docker run -d --rm --runtime nvidia -v ${PATH_FOR_INPUT_IMAGES_FOLDER}:/storage ${DOCKER_IMAGE_NAME} --config ${FILE_NAME: default=config.list} --image ${PATH_TO_AN_IMAGE}
```

The result of the inference is an image, and the image is stored in `/storage/${OUTPUT_DIR}`.
