from ..runtime.factory import Registry

DATASET_REGISTRY = Registry('DATASET')


def build_dataset(_type: str, *args, **kwargs) -> object:
    return DATASET_REGISTRY.get(_type)(*args, **kwargs)
