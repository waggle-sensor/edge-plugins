### Let's start training a semantic segmentation deep learning model
  
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

For internal users who has access to the Alien Machine, users can copy images from `/storage/sunspot/resized/train`. The RGB images are stored in `images` folder, and labeled images are stored in `gt_images`. If the name is funcky, we can change this later. 

3) Preparing Class List

With the images,`class_names.list` is required. The list need to be stored in the same folder where the `images` and `gt_images` exist. The `class_names.list` is the name of classes that the users target to train for. For example, to train a model for cloud segmentation, the `class_names.list` will be:
```
sky
cloud
```

4) Preparing Class Color List

If the color of the class follows Pascal or [Cityscape](https://arxiv.org/pdf/1604.01685.pdf) images, or users use waggle cloud images set, then it does not require `class_colors.list` which contians color configuration for each class (R, G, B). However this segmentation version does not support for other color configuration rather than Pascal or Cityscape as for 4/10/2020.


5) Preparing Model Configuration

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


6) Pre-trained models

The plugin requires a pre-trained fcn model with regard to what the user is tyring to train. If the host machine is connected to the internet, it will automatically download the pretrained model from PyTorch server. If users want to provide a pre-trained model, the path of the pretrained model can be listed in the configuration.


7) Check the folder to mount it to docker file

All of the files and folders must be in one folder, and the folder needs to be mounted as `/storage`.

For example:
```
foler
 ├─ images
 │     ├─ image1
 │     ├─ image2
 │     └─ ...      
 ├─ gt_images
 │     ├─ gt_image1
 │     ├─ gt_image2
 │     └─ ...
 ├─ class_names.list
 ├─ class_colors.list (not supported yet)
 └─ config.list
```


8) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct. The folder that contains training data needs to be mounted to `/storage`.

If users use waggle cloud images, then `--image_type` must be `waggle_cloud`.

For example to use waggle cloud images with 16GB shared memory to train resnet-fcn101 network:
```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm \
  --runtime nvidia \
  --shm-size 16G \
  -v ${PATH_FOR_INPUT_IMAGES_FOLDER}:/storage \
  classicblue\plugin-training-fcn:0.2.0 \
  --config config_resnet101.list \ 
  --image_type waggle_cloud
```

9) Check Progress

The log of the training can be shown by,

```
docker logs -f ${DOCKER_IMAGE_NAME or CONTAINER_ID}
```

10) Check Training Logs

After the training is completed checkpoint models and logs can be found in `/storage/${MODEL_NAME}` on the host machine. The logs stored in cvs file, and users can handle the data as they familiar with.
