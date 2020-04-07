import os
import os.path as osp
import torch
import numpy as np

import warnings
warnings.filterwarnings('ignore')

## root folder for the images and label images
root = '/storage'

## read configuration file
import json
with open('/storage/config.list', 'r') as json_file:
    configurations = json.load(json_file)


from types import SimpleNamespace
opts = SimpleNamespace()
opts.cfg = configurations['2']

## read file that contains class names
class_names = []
with open('/storage/class_names.list', 'r') as f:
    for line in f:
        class_names.append(line.strip())

class_names = np.array(class_names)
print(class_names)

cuda = torch.cuda.is_available()
print(cuda)
opts.cuda = 'cuda' if cuda else 'cpu'
opts.mode = 'train'

opts.n_classes = len(class_names)
opts.backbone = opts.cfg['backbone']
opts.fcn = opts.cfg['fcn']
opts.cfg['cuda'] = opts.cuda
opts.cfg['mode'] = opts.mode
opts.cfg['n_classes'] = opts.n_classes
#opts.backbone = 'resnet'
#opts.fcn = '101'

import datetime
now = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
opts.cfg['utc_time'] = now


opts.resume = ''

def get_log_dir(model_name, config_id, cfg):
    # load config
    #import datetime
    # import pytz
    import os
    import yaml
    import os.path as osp
    name = 'MODEL-%s' % (model_name)
    # now = datetime.datetime.now(pytz.timezone('America/Bogota'))
    # name += '_TIME-%s' % now.strftime('%Y%m%d-%H%M%S')
    # create out
    log_dir = osp.join('logs', name)
    if not osp.exists(log_dir):
        os.makedirs(log_dir)
    with open(osp.join(log_dir, 'config.yaml'), 'w') as f:
        yaml.safe_dump(cfg, f, default_flow_style=False)
    return log_dir

opts.out = get_log_dir(opts.cfg['log_dir'], 1, opts.cfg)
#opts.out = get_log_dir('resnet101', 1, opts.cfg)

print(opts.cfg)


from data_loader import Cloud_Data
kwargs = {'num_workers': 4} if cuda else {}
train_loader = torch.utils.data.DataLoader(
    Cloud_Data(
        class_names,
        root,
        image_set='train',
        backbone=opts.backbone,
        transform=True),
    batch_size=1,
    shuffle=True,
    **kwargs
)

val_loader = torch.utils.data.DataLoader(
    Cloud_Data(
        class_names,
        root,
        image_set='val',
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
