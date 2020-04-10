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

Waggle team will provide an example dataset for cloud segmentation for users of this plugin. Users can download the images from google drive or relavant method:
```
download from somewhare that we are going to provide
```

The RGB images must be stored in ```image``` folder, and labeled images must be stored in ```gt_image```. If the name is funcky, we can change this later. Recommended number of images is 1,000 per classes according to TensorFlow, but user can try with less number of images.

With the images, two additional files must be stored in the same folder where the ```image``` and ```gt_image``` exist, which are ```config.list``` (can be any other name) and ```class_names.list``` (must be this name).

The ```config.list``` is the configuration of the training such as maximum iteration (```max_iteration```), learning rate (```lr```),  backbone network of the trainig (```backbone```), and so on. An example of a configuration for training Resnet based fcn101 network is provided below: 
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

The ```class_names.list``` is for the .......




  
  1. Download sky images from waggle repository (will be added the images and labeled images for training 4/7/2020).
  2. Store the data, configuration file, and a list of class names in one folder named ```/storage```.
  3. Download the docker file from docker hub (will be added on waggle docker hub 4/7/2020).
  4. Run the docker through the command below (will be added 4/7/2020)
