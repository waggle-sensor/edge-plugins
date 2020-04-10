### Let's start training a semantic segmentation deep learning model
  
The plugin runs PyTorch based FCN models for traning. To run the plugin, users must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.
  
1) Preparing Docker

Docker is a set of platform as a service products that uses OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries, and configuration files.

Users can install the docker in their machine through the APIs that are provided by docker. Go to the website and install the docker on your device with regard to your OS.
```
https://docs.docker.com/get-docker/
```

If users already have or installed docker, then you can download our docker file:
```
docker pull classicblue/plugin-pytorch-fcn
```

2) Preparing Dataset

Waggle team will provide an example dataset for cloud segmentation for users of this plugin. Users can download the images from google drive or relevant method:
```
download from somewhare that we are going to provide
```

For internal users who has access to the Alien Machine, The images are in `/storage/sunspot/resized/train/images`.

The RGB images must be stored in `images` folder, and labeled images must be stored in `gt_images`. If the name is funcky, we can change this later. Recommended number of images is 1,000 per classes according to TensorFlow, but user can try with less number of images.

With the images,`class_names.list` is required to be stored in the same folder where the `images` and `gt_images` exist. The `class_names.list` is the name of classes that the users target to train for. For example, to train a model for cloud segmentation, the `class_names.list` will be:
```
sky
cloud
```

If the color of the class follows Pascal or [Cityscape](https://arxiv.org/pdf/1604.01685.pdf) images, then it does not require `color_names.list` which contians color configuration for each class (R, G, B). However the docker does not support for other color configuration rather than Pascal or Cityscape yet.


3) Preparing Model Configuration

The `config.list` is the configuration of the training such as maximum iteration (`max_iteration`), learning rate (`lr`),  director name for saving logs and models under `/storage` folder (`log_dir`), and so on. An example of a configuration for training Resnet based fcn101 network is provided below: 
```
{
    "max_iteration": 100000, 
    "lr": 1e-10, 
    "momentum": 0.99, 
    "weight_decay": 0.0005, 
    "interval_validate": 4000,
    "backbone": "resnet",
    "fcn": "101",
    "log_dir": "resnet101"
}
```

For now (4/10/2020) the docker file provides Resnet as backbone network, and fcn101 and fcn50 as fcn network. So user can choose either resnet-fcn101 or resent-fcn50.


4) Pre-trained models

The plugin requires a pre-trained fcn model with regard to what the user is tyring to train. If the host machine is connected to the internet, it will automatically download the pretrained model from PyTorch server. If users want to provide a pre-trained model, the path of the pretrained model can be listed in the configuration.


**All of the files and folders must be in one folder, and the folder needs to be mounted as `/storage`**


5) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct.


```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm \
  --runtime nvidia \
  --shm-size 16G \
  -v ${PATH_FOR_INPUT_IMAGES_FOLDER}:/storage \
  ${DOCKER_IMAGE_NAME} \
  --config ${FILE_NAME: default=config.list} 
  --image_type ${SEGMENTATION_CLASS_COLORING_TYPE: default=voc}
```

The log of the training can be shown by,

```
docker logs -f ${DOCKER_IMAGE_NAME}
```

After the training is completed checkpoint models and logs can be found in `/storage/${MODEL_NAME}` on the host machine. The logs can be rendered by `tensorboard`.

```
$ tensorboard --logdir ${PATH_TO_LOGS}
```
