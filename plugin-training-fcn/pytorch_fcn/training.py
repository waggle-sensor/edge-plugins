import os
import os.path as osp
import yaml

import torch
import numpy as np

import warnings
warnings.filterwarnings('ignore')

import argparse
import json

from types import SimpleNamespace
import datetime

from data_loader import Cloud_Data
from trainer import Trainer


def get_log_dir(model_name, config_id, cfg, root):
    name = 'MODEL-%s' % (model_name)
    log_dir = root + name
    if not osp.exists(log_dir):
        os.makedirs(log_dir)
    with open(osp.join(log_dir, 'config.list'), 'w') as f:
        yaml.safe_dump(cfg, f, default_flow_style=False)
    return log_dir


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--config', type=str, default='config.list', help='path to train configuration list')
    parser.add_argument('--image_type', type=str, default='voc', help='segmentation class coloring type')
    args = parser.parse_args()

    ## root folder for the images and label images
    root = '/storage/'
    args.config = root + args.config

    ## read configuration file
    with open(args.config, 'r') as f:
        configurations = json.load(f)

    opts = SimpleNamespace()
    opts.cfg = configurations

    #print(opts.cfg)

    if opts.cfg['backbone'] != 'ressnet':
        raise Exception('Not supported')


    ## read file that contains class names
    class_names = []
    with open('/storage/class_names.list', 'r') as f:
        for line in f:
            class_names.append(line.strip())

    class_names = np.array(class_names)
    #print(class_names)

    cuda = torch.cuda.is_available()
    #print(cuda)

    opts.cfg['cuda'] = 'cuda' if cuda else 'cpu'
    opts.cfg['mode'] = 'train'
    opts.cfg['n_classes'] = len(class_names)

    #opts.cfg['pretrained'] = ''

    '''
    opts.resume = ''
    '''

    now = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    opts.cfg['utc_time'] = now

    opts.out = get_log_dir(opts.cfg['output_dir'], 1, opts.cfg, root)

    #print(opts.cfg)


    kwargs = {'num_workers': opts.cfg['n_workers']} if cuda else {}
    train_loader = torch.utils.data.DataLoader(
        Cloud_Data(
            class_names,
            root,
            args.image_type,
            image_set='train',
            backbone=opts.cfg['backbone'],
            transform=True),
        batch_size=opts.cfg['batch_size'],
        shuffle=True,
        **kwargs
    )

    val_loader = torch.utils.data.DataLoader(
        Cloud_Data(
            class_names,
            root,
            args.image_type,
            image_set='val',
            backbone=opts.cfg['backbone'],
            transform=True),
        batch_size=opts.cfg['batch_size'],
        shuffle=False,
        **kwargs
    )
    data_loader=[train_loader,val_loader]

    trainer = Trainer(data_loader, opts)

    start_epoch = 0
    start_iteration = 0
    '''
    if opts.resume:
        start_epoch = checkpoint['epoch']
        start_iteration = checkpoint['iteration']
    '''
    trainer.epoch = start_epoch
    trainer.iteration = start_iteration
    trainer.Train()
