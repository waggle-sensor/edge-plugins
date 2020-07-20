## Train Resnet-FCN network on PyTorch and Test the Model
The plugin trains unet model and tests the models. To run the plugin, the user must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.


### Train a Model

0) Download Docker image

```
docker pull waggle/plugin-training-unet
```

1) Preparing Dataset

Image dataset including labeled images needs to be prepared on the host machine and the root path of the dataset needs to be mounted onto the plugin container. For training, the following files and folders need to be prepared as well.

- `train/images` is a folder containing all images
- `train/labels` is a folder containing all labeled (ground truth) images

Recommended number of images is 1,000 per classes according to TensorFlow, but user can try with less number of images. The ground truth images (labeled images) must be binary (0 or 255).

**Waggle team provides an example dataset for cloud segmentation for users of this plugin.**

Any person using the Data, shall not distribute, share, publish or release the Data to any person. The Data will only be used in research and the user may not make copies of the data for use outside of its research responsibilities.

Users can download the images through below:
```
from torchvision.datasets.utils import download_and_extract_archive
url = 'https://web.lcrc.anl.gov/public/waggle/datasets/WaggleClouds-0.2.0.tar.gz'
download_and_extract_archive(url, 'download', 'data')
```

2) Model Configuration

User can change parameters that are listed below as input arguments:
```
## For train
'-e', '--epochs', metavar='E', type=int, default=5, help='Number of epochs', dest='epochs'
'-b', '--batch-size', metavar='B', type=int, nargs='?', default=1, help='Batch size', dest='batch_size'
'-l', '--learning-rate', metavar='LR', type=float, nargs='?', default=0.00001, help='Learning rate', dest='lr'
'-w', '--weights', nargs='*', help='Class weights to use in loss calculation'
'--n_channels', type=int, default=3, help='Number of channels in input images'
'-f', '--load', dest='load', type=str, default=False, help='Load model from a .pth file'
'-v', '--validation', dest='val', type=float, default=10.0, help='Percent of the data that is used as validation (0-100)'

## for both train and inference
'-d', '--mode', dest='mode', type=str, default='train', help='Mode to run the U-Net, train or infer'
'-s', '--scale', dest='scale', type=float, default=0.5, help='Downscaling factor of the images'
'--n_classes', type=int, default=1, help='Number of classes in the segmentation'

```

Basically number of workers for loading images is 8. **`n_workers` in the configuration will be added.**

3) Pretrained models

The plugin can load a pre-trained model.  If users want to provide a pre-trained model, the path of the pretrained model can be provided through `-f` or `--load` argument for training, and `-m` or `--model` argument for inference.


**All of the files and folders must be in one folder, and the folder needs to be mounted as `/data`**

All of the files and folders must be in one folder. For example:
```
input foler
 ├─ train
 │     ├─ images
 │     │     ├─ image1
 │     │     ├─ image2
 │     │     └─ ...
 │     └─ labels
 │           ├─ image1
 │           ├─ image2
 │           └─ ...
 └─ pretrained_model (optional, such as model_best.pth) ## not yet tested
 
 
output folder
 ├─ runs
 │     ├─ tensorboard log1
 │     ├─ tensorboard log2
 │     └─ ...
 │     └─ labels
 └─ checkpoints
       ├─ checkpoint1
       ├─ checkpoint2
       └─ ...
 ```

4) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct.


```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm \
 --runtime nvidia \
 --shm-size 16G \
 -v ${PATH_TO_IMAGES}:/data \
 -v ${PATH_TO_CHECKPOINT}:/train/checkpoints \
 -v ${PATH_TO_LOGS}:/train/runs \
 classicblue/plugin-training-unet \
 -d train \
 -e 5 \
 -l 0.00006 \
 -b 4 \
 -s 1.0
```

The `--runtime nvidia` option is for old version of nvidia-docker runtime toolkit. For the users who are using newest version of nvidia-docker runtime toolkit, use option of `--gpus all` instead of `--runtime nvidia`.

The log of the training can be shown by,

```
docker logs -f ${DOCKER_IMAGE_NAME}
```

After the training is completed checkpoint models and logs can be found in `${PATH_TO_CHECKPOINT}` on the host machine. The logs stored in `${PATH_TO_LOGS}` as tensorboard and csv file, and users can handle the data as they familiar with.



### Test the Model


1) Inference Configuration

User can change parameters that are listed below as input arguments:
```
## for both train and inference
'-d', '--mode', dest='mode', type=str, default='train', help='Mode to run the U-Net, train or infer'
'-s', '--scale', dest='scale', type=float, default=0.5, help='Downscaling factor of the images'
'--n_classes', type=int, default=1, help='Number of classes in the segmentation'

## for inference
'-m', '--model', metavar='FILE', help='Specify the file in which the model is stored'
'-i', '--input', metavar='INPUT', default='/data/test/', help='Folder to read input images'
'-o', '--output', metavar='OUTPUT', default='/train/output/', help='Folder to save ouput images'
'-n', '--no-save', action='store_true', default=False, help='Do not save the output masks'
'-t', '--mask-threshold', type=float, default=0.5, help='Minimum probability value to consider a mask pixel white')
```


2) Trained model

The plugin can load a pre-trained model.  If users want to provide a pre-trained model, the path of the pretrained model can be provided through `-f` or `--load` argument for training, and `-m` or `--model` argument for inference.


3) Preparing Images

The plugin requires a folder that containes images for inference, and it assumes that the image is stored in `test/images`.

**All of the files and folders must be in one folder, and the folder needs to be mounted as `/data`. The Docker image assumes that the config.list and the trained model are in under `/data`** like below:

```
input foler
 └─ test
       └─ images
             ├─ image1
             ├─ image2
             └─ ...
             
 
output folder
 └─ checkpoints
         ├─ checkpoint1
         ├─ checkpoint2
         └─ ...
 
 output image folder
   └─ output images
         ├─ output1
         ├─ output2
         └─ ...
```

4) Inference

To inference, simply run the command below on the host machine. Please make sure to set all the path correct.


```
docker run -d --rm \
 --runtime nvidia \
 --shm-size 16G \
 -v ${PATH_TO_IMAGES}:/data \
 -v ${PATH_TO_CHECKPOINT}:/train/checkpoints \
 -v ${PATH_TO_OUTPUT_IMAGES}:/train/output \
 classicblue/plugin-training-unet \
 -d test \
 -s 1.0
```

The result of the inference is an image, and the image is stored in `${OUTPUT_DIR}`.

### Acknowledgement

This repo is built upon [tim-vdl](https://github.com/tim-vdl/Pytorch-UNet)'s code and some snippets can be just a mirror.

