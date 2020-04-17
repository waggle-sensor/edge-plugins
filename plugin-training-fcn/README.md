### Training Resnet-FCN network on PyTorch
The plugin trains fcn models: resnet101 based fcn101 and fcn50. To run the plugin, the user must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.

1) Preparing Dataset

Image dataset including labeled images needs to be prepared on the host machine and the root path of the dataset needs to be mounted onto the plugin container. For training, the following files and folders need to be prepared as well.

- `images` is a folder containing all images
- `labels` is a folder containing all labeled (ground truth) images
- `class_names.list` is a file containing class names; one class name per line
- `color_names.list` is a file containing RGB color value for each class; one class color set per line (R, G, B) **Will be supported**

Recommended number of images is 1,000 per classes according to TensorFlow, but user can try with less number of images. The ground truth images (labeled images) must follow Pascal or [Cityscape](https://arxiv.org/pdf/1604.01685.pdf) lable in terms of coler of class. Data_loader for other class definition type is not ready (4/10/2020).

2) Preparing Model Configuration

- `config.list` (or other file name that user named) is a file containing configuration of the training as shown below; user can add additional configuration for their use (The possible pair of backbone and fcn are: `{resnet, 101}, {resnet, 50}:
```
{
    "max_iteration": 100000, 
    "lr": 1e-10, 
    "momentum": 0.99, 
    "weight_decay": 0.0005, 
    "interval_validate": 4000,
    "backbone": "resnet",
    "fcn": "101",
    "output_dir": "resnet101",
    "pretrained_net": "", 
}
```

3) Pretrained models

The plugin requires a pre-trained fcn model with regard to what the user is tyring to train. If the host machine is connected to the internet, it will automatically download the pretrained model from PyTorch server. If users want to provide a pre-trained model, the path of the pretrained model can be listed in the configuration.

- `pretrained_net` in configuration is a path to a prerained PyTorch model such as resnet101_from_caffe.pth


**All of the files and folders must be in one folder, and the folder needs to be mounted as `/storage`**


4) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct.


```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm --runtime nvidia --shm-size 16G -v ${PATH_FOR_INPUT_IMAGES_FOLDER}:/storage ${DOCKER_IMAGE_NAME} --config ${FILE_NAME: default=config.list} --image_type ${SEGMENTATION_CLASS_COLORING_TYPE: default=voc}
```

The log of the training can be shown by,

```
docker logs -f ${DOCKER_IMAGE_NAME}
```

After the training is completed checkpoint models and logs can be found in `/storage/${MODEL_NAME}` on the host machine. The logs stored in csv file, and users can handle the data as they familiar with.



### Adjustment required:

- Adapt color set that is not Pascal or Cityscape.

