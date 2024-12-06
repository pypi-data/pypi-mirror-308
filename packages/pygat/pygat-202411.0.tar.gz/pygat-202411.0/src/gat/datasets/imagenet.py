from pathlib import Path
from typing import List, Union

import torch
import torchvision

from .builder import DATASET_REGISTRY
from .transforms import resize_256_224, to_color, to_ts


@DATASET_REGISTRY.register()
def imagenet(
    data_root: Union[str, Path],
    is_train: bool = True,
    filter_class: Union[int, List[int]] = None,
) -> torch.utils.data.Dataset:
    if isinstance(data_root, str):
        data_root = Path(data_root)
    if is_train:
        data_root = data_root / 'train'
    else:
        data_root = data_root / 'val'

    _transforms = resize_256_224() + to_color() + to_ts()

    _ds = torchvision.datasets.ImageFolder(
        data_root,
        transform=torchvision.transforms.Compose(_transforms),
    )

    if isinstance(filter_class, int):
        filter_class = [filter_class]
    if filter_class:
        _ds.samples = list(filter(lambda x: x[1] in filter_class, _ds.samples))

    return _ds
