from ...runtime.factory import Registry

SURROGATE_REGISTRY = Registry('SURROGATE')


def build_surrogate(_type: str, *args, **kwargs) -> object:
    return SURROGATE_REGISTRY.get(_type)(*args, **kwargs)


def list_surrogates():
    return list(SURROGATE_REGISTRY._obj_map.keys())
