from solver import solver
import datetime
import os.path as osp
import torch
import numpy as np
import tqdm
import fcn
import math
#import pytz
import os
import imageio
import shutil


class Trainer(solver):
    def __init__(self, data_loader, opts):
        super(Trainer, self).__init__(data_loader, opts)
        self.cuda = opts.cfg['cuda']
        self.opts = opts
        self.train_loader = data_loader[0]
        self.val_loader = data_loader[1]

        if opts.cfg['mode'] in ['val']:
            return

        ## UTC time
        #self.timestamp_start = \
        #    datetime.datetime.now(pytz.timezone('America/Bogota'))
        self.timestamp_start = \
            datetime.datetime.now()

        self.interval_validate = opts.cfg.get('interval_validate',
                                              len(self.train_loader))
        if self.interval_validate is None:
            self.interval_validate = len(self.train_loader)

        self.out = opts.out
        if not osp.exists(self.out):
            os.makedirs(self.out)

        self.log_headers = [
            'epoch',
            'iteration',
            'train/loss',
            'train/acc',
            'train/acc_cls',
            'train/mean_iu',
            'train/fwavacc',
            'valid/loss',
            'valid/acc',
            'valid/acc_cls',
            'valid/mean_iu',
            'valid/fwavacc',
            'elapsed_time',
        ]
        if not osp.exists(osp.join(self.out, 'log.csv')):
            with open(osp.join(self.out, 'log.csv'), 'w') as f:
                f.write(','.join(self.log_headers) + '\n')

        self.epoch = 0
        self.iteration = 0
        self.max_iter = opts.cfg['max_iteration']
        self.best_mean_iu = 0


    def _fast_hist(self, label_true, label_pred, n_class):
        mask = (label_true >= 0) & (label_true < n_class)
        hist = np.bincount(n_class * label_true[mask].astype(int) +
                       label_pred[mask],
                       minlength=n_class**2).reshape(n_class, n_class)
        return hist


    def _label_accuracy_score(self, label_trues, label_preds, n_class):
        """Returns accuracy score evaluation result.
          - overall accuracy
          - mean accuracy
          - mean IU
          - fwavacc
        """
        hist = np.zeros((n_class, n_class))
        for lt, lp in zip(label_trues, label_preds):
            hist += self._fast_hist(lt.flatten(), lp.flatten(), n_class)
        acc = np.diag(hist).sum() / hist.sum()
        acc_cls = np.diag(hist) / hist.sum(axis=1)
        acc_cls = np.nanmean(acc_cls)
        iu = np.diag(hist) / (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist))
        mean_iu = np.nanmean(iu)
        freq = hist.sum(axis=1) / hist.sum()
        fwavacc = (freq[freq > 0] * iu[freq > 0]).sum()
        return acc, acc_cls, mean_iu, fwavacc



    def validate(self):
        # import matplotlib.pyplot as plt
        training = self.model.training
        self.model.eval()

        n_class = len(self.val_loader.dataset.class_names)

        val_loss = 0
        visualizations = []
        label_trues, label_preds = [], []
        with torch.no_grad():
            for batch_idx, (data, target) in tqdm.tqdm(
                    enumerate(self.val_loader),
                    total=len(self.val_loader),
                    desc='Valid iteration=%d' % self.iteration,
                    ncols=80,
                    leave=False):
                #print(target)
                data, target = data.to(self.cuda, dtype=torch.float), target.to(self.cuda)
                score = self.model(data)

                ############################################################################################### for test 4/6/2020
                #raise Exception(data.shape, target.shape)

                loss = self.cross_entropy2d(score, target)
                if np.isnan(float(loss.item())):
                    raise ValueError('loss is nan while validating')
                val_loss += float(loss.item()) / len(data)

                imgs = data.data.cpu()
                lbl_pred = score.data.max(1)[1].cpu().numpy()[:, :, :]
                lbl_true = target.data.cpu()
                for img, lt, lp in zip(imgs, lbl_true, lbl_pred):
                    img, lt = self.val_loader.dataset.untransform(img, lt)
                    label_trues.append(lt)
                    label_preds.append(lp)
                    if len(visualizations) < 9:
                        viz = fcn.utils.visualize_segmentation(lbl_pred=lp,
                                                               lbl_true=lt,
                                                               img=img,
                                                               n_class=n_class)
                        visualizations.append(viz)
        metrics = self._label_accuracy_score(label_trues, label_preds, n_class)

        out = osp.join(self.out, 'visualization_viz')
        if not osp.exists(out):
            os.makedirs(out)
        out_file = osp.join(out, 'iter%012d.jpg' % self.iteration)
        #raise Exception(len(visualizations))
        img_ = fcn.utils.get_tile_image(visualizations)
        imageio.imwrite(out_file, img_)
        # plt.imshow(imageio.imread(out_file))
        # plt.show()

        val_loss /= len(self.val_loader)

        with open(osp.join(self.out, 'log.csv'), 'a') as f:
            elapsed_time = (
                datetime.datetime.now() -
                self.timestamp_start).total_seconds()
            log = [self.epoch, self.iteration] + [''] * 5 + \
                  [val_loss] + list(metrics) + [elapsed_time]
            log = map(str, log)
            f.write(','.join(log) + '\n')

        mean_iu = metrics[2]
        is_best = mean_iu > self.best_mean_iu
        if is_best:
            self.best_mean_iu = mean_iu
        torch.save(
            {
                'model': self.model,
                'epoch': self.epoch,
                'iteration': self.iteration,
                'arch': self.model.__class__.__name__,
                'optim_state_dict': self.optim.state_dict(),
                'model_state_dict': self.model.state_dict(),
                'best_mean_iu': self.best_mean_iu,
            }, osp.join(self.out, 'checkpoint.pth.tar'))
        if is_best:
            shutil.copy(osp.join(self.out, 'checkpoint.pth.tar'),
                        osp.join(self.out, 'model_best.pth.tar'))

        if training:
            self.model.train()

    def train_epoch(self):
        self.model.train()

        n_class = len(self.train_loader.dataset.class_names)

        for batch_idx, (data, target) in tqdm.tqdm(
                enumerate(self.train_loader),
                total=len(self.train_loader),
                desc='Train epoch=%d' % self.epoch,
                ncols=80,
                leave=False):
            iteration = batch_idx + self.epoch * len(self.train_loader)
            if self.iteration != 0 and (iteration - 1) != self.iteration:
                continue  # for resuming
            self.iteration = iteration

            if self.iteration % self.interval_validate == 0:
                self.validate()

            assert self.model.training

            data, target = data.to(self.cuda), target.to(self.cuda)
            self.optim.zero_grad()
            score = self.model(data)

            loss = self.cross_entropy2d(score, target)
            loss /= len(data)
            if np.isnan(float(loss.item())):
                raise ValueError('loss is nan while training')
            loss.backward()
            self.optim.step()

            metrics = []
            lbl_pred = score.data.max(1)[1].cpu().numpy()[:, :, :]
            lbl_true = target.data.cpu().numpy()
            acc, acc_cls, mean_iu, fwavacc = \
                self._label_accuracy_score(
                    lbl_true, lbl_pred, n_class=n_class)
            metrics.append((acc, acc_cls, mean_iu, fwavacc))
            metrics = np.mean(metrics, axis=0)

            with open(osp.join(self.out, 'log.csv'), 'a') as f:
                elapsed_time = (
                    datetime.datetime.now() -
                    self.timestamp_start).total_seconds()
                log = [self.epoch, self.iteration] + [loss.item()] + \
                    metrics.tolist() + [''] * 5 + [elapsed_time]
                log = map(str, log)
                f.write(','.join(log) + '\n')

            if self.iteration >= self.max_iter:
                break

    def Train(self):
        max_epoch = int(math.ceil(1. * self.max_iter / len(self.train_loader)))
        for epoch in tqdm.trange(self.epoch, max_epoch, desc='Train',
                                 ncols=80):
            self.epoch = epoch
            self.train_epoch()
            if self.iteration >= self.max_iter:
                break


    '''
    def _run_fromfile(self, model, img_file, cuda, transform, val=False):
        import matplotlib.pyplot as plt
        import torch
        if not val:
            img_torch = torch.unsqueeze(fileimg2model(img_file, transform), 0)
        else:
            img_torch = img_file
        img_torch = img_torch.to(cuda)
        model.eval()
        with torch.no_grad():
            if not val:
                img_org = plt.imread(img_file)
            else:
                img_org = transform(img_file[0], img_file[0])[0]

            score = model(img_torch)
            lbl_pred = score.data.max(1)[1].cpu().numpy()

            plt.imshow(img_org, alpha=.9)
            imshow_label(lbl_pred[0], alpha=0.5)
            plt.show()



    def Test(self):
        for image, label in self.val_loader:
            self._run_fromfile(self.model,
                         image,
                         self.opts.cuda,
                         self.val_loader.dataset.untransform,
                         val=True)

    def Demo(self):
        import glob
        img_files = sorted(glob.glob('imgs/*.jpg'))
        for img in img_files:
            self._run_fromfile(self.model, img, self.opts.cuda,
                         self.val_loader.dataset.transforms)
    '''
