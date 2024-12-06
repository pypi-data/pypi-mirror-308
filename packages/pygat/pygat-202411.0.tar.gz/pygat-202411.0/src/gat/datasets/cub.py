from .builder import DATASET_REGISTRY


@DATASET_REGISTRY.register()
def cub():
    raise NotADirectoryError
