import os
import os.path as osp
import torch
import warnings
warnings.filterwarnings('ignore')

configurations={
    1: dict(
        max_iteration=100000,
        lr=1.0e-10,
        momentum=0.99,
        weight_decay=0.0005,
        interval_validate=4000,
    )
}

from types import SimpleNamespace
opts = SimpleNamespace()
opts.cfg = configurations[1]
opts.resume = ''

from utils import get_log_dir
opts.out = get_log_dir('resnet101', 1, opts.cfg)
print(opts.cfg)
cuda = torch.cuda.is_available()
cuda = False
print(cuda)
opts.cuda = 'cuda' if cuda else 'cpu'
opts.mode = 'train'
opts.backbone = 'resnet'
opts.fcn = '101'
root = './data/Pascal_VOC'
root_swim = './data/cloud/cce/swimseg'
root_hyta = './data/cloud/cce/HYTA'

from cl_data_loader import Cloud_Data
kwargs = {'num_workers': 4} if cuda else {}
train_loader = torch.utils.data.DataLoader(
    Cloud_Data(
        root_swim,
        image_set='train',
        backbone=opts.backbone,
        transform=True),
    batch_size=1,
    shuffle=True,
    **kwargs
)

val_loader = torch.utils.data.DataLoader(
    Cloud_Data(
        root_swim,image_set='val',
        backbone=opts.backbone,
        transform=True),
    batch_size=1,
    shuffle=False,
    **kwargs
)
data_loader=[train_loader,val_loader]

from trainer import Trainer
trainer = Trainer(data_loader, opts)

start_epoch = 0
start_iteration = 0
if opts.resume:
    start_epoch = checkpoint['epoch']
    start_iteration = checkpoint['iteration']

trainer.epoch = start_epoch
trainer.iteration = start_iteration
trainer.Train()
