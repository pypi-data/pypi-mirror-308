from typing import List

import torchvision

from . import env


def resize_256_224() -> List:
    return [
        torchvision.transforms.Resize(size=256),
        torchvision.transforms.CenterCrop(size=(224, 224)),
    ]


def resize_512_448() -> List:
    return [
        torchvision.transforms.Resize(size=512),
        torchvision.transforms.CenterCrop(size=(448, 448)),
    ]


def resize_224() -> List:
    return [torchvision.transforms.Resize(size=224)]


def hflip() -> List:
    return [torchvision.transforms.RandomHorizontalFlip(0.5)]


def to_ts() -> List:
    return [torchvision.transforms.ToTensor()]


def to_pil() -> List:
    return [torchvision.transforms.ToPILImage()]


def to_color() -> List:
    return [
        torchvision.transforms.Lambda(lambda x: x.convert('RGB')
                                      if x.mode != 'RGB' else x)
    ]


def norm(dataset: str = 'IMAGENET', _callable: bool = False) -> List:
    dataset = dataset.upper()
    assert dataset in ['CIFAR10', 'CIFAR100', 'IMAGENET']
    mean_std = (
        getattr(env, dataset + '_DEFAULT_MEAN'),
        getattr(env, dataset + '_DEFAULT_STD'),
    )
    transforms = [torchvision.transforms.Normalize(*mean_std)]
    if _callable:
        return torchvision.transforms.Compose(transforms)
    return transforms
