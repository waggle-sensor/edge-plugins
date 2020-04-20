class solver(object):
    def __init__(self, data_loader, opts):
        from importlib import import_module
        self.data_loader = data_loader

        model_module = import_module('models.{}.fcn{}'.format(opts.cfg['backbone'], opts.cfg['fcn']))
        self.model = model_module.FCN(n_class=opts.cfg['n_classes'])

        self.model.resume(opts.cfg['pretrained'])

        optim_module = import_module('models.{}.helpers'.format(opts.cfg['backbone']))
        self.optim = optim_module.prepare_optim(opts, self.model)

        self.model.to(opts.cfg['cuda'])

    def cross_entropy2d(self, input, target, weight=None):
        # Softmax + Negative Log Likelihood
        import torch.nn.functional as F
        # input: (n, c, h, w), target: (n, h, w)
        n, c, h, w = input.size()
        # log_p: (n, c, h, w)
        log_p = F.log_softmax(input, dim=1)
        # log_p: (n*h*w, c)
        log_p = log_p.transpose(1, 2).transpose(2, 3).contiguous()
        log_p = log_p[target.view(n, h, w, 1).repeat(1, 1, 1, c) >= 0]
        log_p = log_p.view(-1, c)
        # target: (n*h*w,)
        mask = target >= 0
        target = target[mask]
        loss = F.nll_loss(log_p, target, weight=weight, reduction='sum')
        #loss /= mask.data.sum()
        return loss

