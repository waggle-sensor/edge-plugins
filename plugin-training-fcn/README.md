## Train Resnet-FCN network on PyTorch and Test the Model
The plugin trains fcn models and tests the models: resnet101 based fcn101 and fcn50. To run the plugin, the user must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.


### Train a Model

1) Preparing Dataset

Image dataset including labeled images needs to be prepared on the host machine and the root path of the dataset needs to be mounted onto the plugin container. For training, the following files and folders need to be prepared as well.

- `train/images` is a folder containing all images
- `train/labels` is a folder containing all labeled (ground truth) images
- `class_names.list` is a file containing class names; one class name per line
- `color_names.list` is a file containing RGB color value for each class; one class color set per line (R, G, B) **Will be supported**

Recommended number of images is 1,000 per classes according to TensorFlow, but user can try with less number of images. The ground truth images (labeled images) must follow Pascal or [Cityscape](https://arxiv.org/pdf/1604.01685.pdf) lable in terms of coler of class. Data_loader for other class definition type is not ready (4/10/2020).

2) Preparing Model Configuration

- `config.list` (or other file name that user named) is a file containing configuration of the training as shown below; user can modify configuration for their use (The possible pair of backbone and fcn are: `{resnet, 101}, {resnet, 50}:
```
{
    "max_iteration": 100000, 
    "lr": 1e-10, 
    "momentum": 0.99, 
    "weight_decay": 0.0005, 
    "interval_validate": 4000,
    "batch_size": 1,
    "backbone": "resnet",
    "fcn": "101",
    "output_dir": "resnet101",
    "pretrained_net": "",
    "n_workers": 6,
    "mode": "train"
}
```

`n_workers` in the configuration is how many workers will be used for read images to reduce time for reading images.

3) Pretrained models

The plugin requires a pre-trained fcn model with regard to what the user is tyring to train. If the host machine is connected to the internet, it will automatically download the pretrained model from PyTorch server. If users want to provide a pre-trained model, the path of the pretrained model can be listed in the configuration.

- `pretrained_net` in configuration is a path to a prerained PyTorch model such as resnet101_from_caffe.pth


**All of the files and folders must be in one folder, and the folder needs to be mounted as `/data`**

All of the files and folders must be in one folder. For example:
```
foler
 ├─ train
 │     ├─ images
 │     │     ├─ image1
 │     │     ├─ image2
 │     │     └─ ...
 │     └─ labels
 │           ├─ image1
 │           ├─ image2
 │           └─ ...
 ├─ class_names.list
 ├─ config.list
 ├─ pretrained_model (optional, such as model_best.pth.tar)
 └─ class_colors.list (not supported yet)
```




4) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct.


```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm --runtime nvidia --shm-size 16G -v ${ROOT_PATH_FOR_CONFIGURATION}:/data waggle/plugin-trainig-fcn --config ${FILE_NAME: default=config.list} --image_type ${SEGMENTATION_CLASS_COLORING_TYPE: default=voc}
```

The log of the training can be shown by,

```
docker logs -f ${DOCKER_IMAGE_NAME}
```

After the training is completed checkpoint models and logs can be found in `/data/${MODEL_NAME}` on the host machine. The logs stored in csv file, and users can handle the data as they familiar with.



### Test the Model


1) Preparing Inference Configuration

- `config.list` (or other file name that user named) is a file containing configuration of the inference as shown below; user can modify configuration for their use (The possible pair of backbone and fcn are: `{resnet, 101}, {resnet, 50}:
```
{
    "backbone": "resnet",
    "fcn": "101",
    "output_dir": "output",
    "model": "resnet_fcn101.pth.tar",
    "mode": "test"
}
```


2) Trained model

The plugin requires a base fcn model with regard to what the user is tyring to inference. The host machine will automatically download the model from PyTorch server. Based on the fcn net, the inference script adds weight from the model that user adds on configuration file, `config.list`. It assumes that the model is stored in the folder where `config.list` is.

- `model` in the configuration is a path to a prerained PyTorch model.



3) Preparing Images

The plugin requires an image for inference, and it assumes that the image is stored in `test/images` folder under the folder where `config.list` is.

**All of the files and folders must be in one folder, and the folder needs to be mounted as `/data`. The Docker image assumes that the config.list and the trained model are in under `/data`** like below:

```
foler
 ├─ test
 │     └─ images
 │           ├─ image1
 │           ├─ image2
 │           └─ ...      
 ├─ class_names.list
 └─ config.list
```


4) Inference

To inference, simply run the command below on the host machine. Please make sure to set all the path correct.


```
docker run -d --rm --runtime nvidia -v ${ROOT_PATH_FOR_CONFIGURATION}:/data waggle/plugin-trainig-fcn --config ${FILE_NAME: default=config.list}
```

The result of the inference is an image, and the image is stored in `/data/test/${OUTPUT_DIR}`.

### Acknowledgement

This repo is built upon [affromero](https://github.com/affromero/FCN)'s code and some snippets can be just a mirror.

### Adjustment required:

- Adapt color set that is not Pascal or Cityscape.

