import os
import os.path as osp

import torch
import numpy as np
import argparse
import json
import datetime

import warnings
warnings.filterwarnings('ignore')

from types import SimpleNamespace

from data_loader import Cloud_Data
from trainer import Trainer

import glob
from PIL import Image
from torchvision import transforms


def get_log_dir(model_name, config_id, cfg, root):
    name = 'MODEL-%s' % (model_name)
    log_dir = root + name
    if not osp.exists(log_dir):
        os.makedirs(log_dir)
    with open(osp.join(log_dir, 'config.list'), 'w') as f:
        f.write(json.dumps(cfg, indent=4, sort_keys=True))
    return log_dir


def train(opts):
    opts.cfg['pretrained'] = root + opts.cfg['pretrained']

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
    if opts.cfg['pretrained']:
        checkpoint = torch.load(opts.cfg['pretrained'])
        start_epoch = checkpoint['epoch']
        start_iteration = checkpoint['iteration']
    '''

    trainer.epoch = start_epoch
    trainer.iteration = start_iteration
    trainer.Train()




def validation(opts):

    ### import FCN module and create model
    from importlib import import_module
    model_module = import_module('models.{}.fcn{}'.format(opts.cfg['backbone'], opts.cfg['fcn']))
    model = model_module.FCN(n_class=int(opts.cfg['n_classes']))


    opts.cfg['model'] = root + opts.cfg['model']

    checkpoint = torch.load(opts.cfg['model'])
    model.load_state_dict(checkpoint['model_state_dict'])



    ### create output directory
    output_base = root + 'test/' + opts.cfg['output_dir']
    if not osp.exists(output_base):
        os.makedirs(output_base)



    # create a color pallette, selecting a color for each class
    palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
    number_of_classes = int(opts.cfg['n_classes'])
    colors = torch.as_tensor([i for i in range(number_of_classes)])[:, None] * palette
    colors = (colors % 255).numpy().astype("uint8")



    ### grap all image files from the image folder
    val_images = glob.glob(root+'test/images/*')
    val_images = val_images[:2]


    for file_path in val_images:
        print(file_path)
        output_name = os.path.basename(file_path) + "_out.jpg"
        output_path = os.path.join(output_base, output_name)

        print(output_path)

        input_image = Image.open(file_path)
        input_image = input_image.resize((300, 300))
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model
        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
           input_batch = input_batch.to('cuda')
           model.to('cuda')
        with torch.no_grad():
            output = model(input_batch)[0]

        output_predictions = output.argmax(0)


        # plot the semantic segmentation predictions of 21 classes in each color
        r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(input_image.size)
        r.putpalette(colors)
        r.convert('RGB').save(output_path)




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


    if opts.cfg['backbone'] != 'resnet':
        raise Exception('Not supported backbone')


    ## read file that contains class names
    class_names = []
    with open('/storage/class_names.list', 'r') as f:
        for line in f:
            class_names.append(line.strip())

    class_names = np.array(class_names)

    cuda = torch.cuda.is_available()
    #print(cuda)

    opts.cfg['cuda'] = 'cuda' if cuda else 'cpu'
    opts.cfg['n_classes'] = len(class_names)


    if opts.cfg['mode'] == 'train':
        train(opts)

    elif opts.cfg['mode'] == 'test':
        validation(opts)

    else:
        raise Exception('Not supported mode')


