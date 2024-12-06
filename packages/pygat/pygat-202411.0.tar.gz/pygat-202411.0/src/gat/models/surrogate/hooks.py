import torch

midlayer_dict = {
    'vgg16': 'features.16',
    'vgg19': 'features.18',
    'resnet152': 'layer2',
    'densenet169': 'features.denseblock2',
    'inception_v3': 'Mixed_6c',
}

feat_collecter = []


def register_collecter(m: torch.nn.Module, layer: str):

    def _hook(m, i, o):
        feat_collecter.append(o)

    _handler = m.get_submodule(layer).register_forward_hook(_hook)
    return _handler, feat_collecter
