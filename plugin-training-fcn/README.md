### Training Resnet101-FCN network on PyTorch
The plugin trains fcn models: resnet101 based fcn101 and fcn50, vgg16 based fcn32, fcn16, and fcn8 (total 5 models). To run the plugin, the user must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.

1) Preparing Dataset

Image dataset needs to be prepared on the host machine and the root path of the dataset will be mounted onto the plugin container. For training labeled images are also required. The following files and folders need to be prepared as well.

- `class_names.list` is a file containing class names; one class name per line
- `image` is a folder containing all images
- `gt_image` is a folder containing all labeled (ground truth) images


2) Preparing Model Configuration

- `config.list` is a file containing configuration of the training as shown below; user can add additional configuration for their use (The possible pair of backbone and fcn are: `{resnet, 101}, {resnet, 50}, {vgg, 32s}, {vgg, 16s}, {vgg, 8s}`:
```
{
    "1": 
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
}
```

**All of the files and folders (total 2 files and 2 folders) must be in one folder, and the folder needs to be mounted as `/storage`**


The plugin requires pre-trained fcn model with regard to what the user is trying to train. The docker will provide the pre-trained models with regard to request.

3) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct.


```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm \
  --runtime nvidia \
  --shm-size 16G \
  .... to be added
  -v ${PATH_FOR_OUTPUT_MODELS}:/plugin/checkpoints \
```

The log of the training can be shown by,

```
docker logs -f .... to be added
```

After the training is completed checkpoint models can be found in `${PATH_FOR_OUTPUT_MODELS}` on the host machine. The logs are saved in `${PATH_TO_LOGS}` and can be rendered by `tensorboard`.

```
$ tensorboard --logdir ${PATH_TO_LOGS}
```

### Adjustment required:

- The code is based on a FCN model that provided by PyTorch so that it is always trying to download the base model from PyTorch server. Therefore, the base model need to be added in the package and the path for the base model needs to be re-identified.

- The path for saving log and model need to be adjust to access outside of the docker.
