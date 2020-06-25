## Train DeepLabv3 (ASPP: Atrous Spatial Pyramid Pooling) network on PyTorch and Test the Model
The plugin trains deeplabv3 model and tests the models. To run the plugin, the user must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.


### Train a Model

0) Download Docker image

```
docker pull waggle/plugin-training-deeplabv3
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
url = 'https://web.lcrc.anl.gov/public/waggle/datasets/WaggleClouds.tar.gz'
download_and_extract_archive(url, 'download', 'data')
```

2) Model Configuration

User can change parameters that are listed below as input arguments:

```
'--mode', type=str, default='train', help='purpose of the run', choices=['train', 'val']

# Datset Options
'--input_path', type=str, help='input dataset path'
'--dataset', type=str, help='Name of dataset', choices=['cityscapes', 'waggle_cloud', 'voc']
'--num_classes', type=int, default=21, help='number of classes (default: None)'
'--resize', type=int, help='resize image'

# Deeplab Options
'--separable_conv', action='store_true', default=False, help='apply separable conv to decoder and aspp'
'--output_stride', type=int, default=16, choices=[8, 16]
'--model', type=str, default='deeplabv3_resnet50', help='model name', choices=['deeplabv3_resnet50',  'deeplabv3plus_resnet50',
                                                                               'deeplabv3_resnet101', 'deeplabv3plus_resnet101',
                                                                               'deeplabv3_mobilenet', 'deeplabv3plus_mobilenet']

# Train Options
'--output', type=str, default='./output', help='folder for output images path'
'--n_workers', type=int, default=4, help='number of workers to read dataset'

'--total_itrs', type=int, default=30e3, help='epoch number (default: 30k)'
'--lr', type=float, default=0.000001, help='learning rate (default: 0.000001)'
'--lr_policy', type=str, default='poly', help='learning rate scheduler policy', choices=['poly', 'step']
'--step_size', type=int, default=10000
'--batch_size', type=int, default=16, help='batch size (default: 16)'
'--interval_val', type=int, default=1000, help='iteration interval for validation'

'--ckpt', default=None, type=str, help='restore from checkpoint'
'--continue_training', action='store_true', default=False

'--loss_type', type=str, default='cross_entropy', help='loss type (default: cross_entropy)', choices=['cross_entropy', 'focal_loss']
'--weight_decay', type=float, default=1e-4, help='weight decay (default: 1e-4)'

```



3) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct.


```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm --runtime nvidia --shm-size 16G -v ${PATH_TO_IMAGES}:/data -v ${PATH_TO_CHECKPOINT}:/train/checkpoints -v ${PATH_TO_LOGS}:/train/runs classicblue/plugin-training-unet -d train -e 5 -l 0.00006 -b 4 -s 1.0
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
# Datset Options
'--input_path', type=str, help='input dataset path'
'--input_file', type=str, help='when a list is an input'
'--num_classes', type=int, default=21, help='number of classes (default: None)'
'--resize', type=int, help='resize image'

# Deeplab Options
'--output_stride', type=int, default=16, choices=[8, 16]
'--model', type=str, default='deeplabv3_resnet50', help='model name', choices=['deeplabv3_resnet50',  'deeplabv3plus_resnet50',
                                                                               'deeplabv3_resnet101', 'deeplabv3plus_resnet101',
                                                                               'deeplabv3_mobilenet', 'deeplabv3plus_mobilenet']

# Inference Options
'--output', type=str, default='./output', help='folder for output images path'
'--n_workers', type=int, default=4, help='number of workers to read dataset'
'--batch_size', type=int, default=16, help='batch size (default: 16)'
'--ckpt', default=None, type=str, help='restore from checkpoint'

```


2) Trained model

The plugin can load a pre-trained model.  If users want to provide a pre-trained model, the path of the pretrained model can be provided through `-f` or `--load` argument for training, and `-m` or `--model` argument for inference.



3) Inference

To inference, simply run the command below on the host machine. Please make sure to set all the path correct.


```
docker run -d --rm --runtime nvidia --shm-size 16G -v ${PATH_TO_IMAGES}:/data -v ${PATH_TO_CHECKPOINT}:/train/checkpoints -v ${PATH_TO_OUTPUT_IMAGES}:/train/output classicblue/plugin-training-unet -d test -s 1.0
```

The result of the inference is an image, and the image is stored in `${OUTPUT_DIR}`.

### Acknowledgement

This repo is built upon [VainF](https://github.com/VainF/DeepLabV3Plus-Pytorch)'s code and some snippets can be just a mirror.
