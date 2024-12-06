import torchvision

from .builder import SURROGATE_REGISTRY

weights_dict = dict(
    vgg16=torchvision.models.VGG16_Weights.IMAGENET1K_V1,
    vgg19=torchvision.models.VGG19_Weights.IMAGENET1K_V1,
    resnet50=torchvision.models.ResNet50_Weights.IMAGENET1K_V1,
    resnet152=torchvision.models.ResNet152_Weights.IMAGENET1K_V1,
    densenet121=torchvision.models.DenseNet121_Weights.IMAGENET1K_V1,
    densenet169=torchvision.models.DenseNet169_Weights.IMAGENET1K_V1,
    inception_v3=torchvision.models.Inception_V3_Weights.IMAGENET1K_V1,
    vit_b_16=torchvision.models.ViT_B_16_Weights.IMAGENET1K_V1,
    vit_b_32=torchvision.models.ViT_B_32_Weights.IMAGENET1K_V1,
    swin_b=torchvision.models.Swin_B_Weights.IMAGENET1K_V1)


@SURROGATE_REGISTRY.register()
def inception_v3(pretrain=True):
    return torchvision.models.inception_v3(
        weights=weights_dict['inception_v3'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def vgg16(pretrain=True):
    return torchvision.models.vgg16(
        weights=weights_dict['vgg16'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def vgg19(pretrain=True):
    return torchvision.models.vgg19(
        weights=weights_dict['vgg19'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def resnet50(pretrain=True):
    return torchvision.models.resnet50(
        weights=weights_dict['resnet50'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def resnet152(pretrain=True):
    return torchvision.models.resnet152(
        weights=weights_dict['resnet152'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def densenet121(pretrain=True):
    return torchvision.models.densenet121(
        weights=weights_dict['densenet121'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def densenet169(pretrain=True):
    return torchvision.models.densenet169(
        weights=weights_dict['densenet169'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def vit_b_16(pretrain=True):
    return torchvision.models.vit_b_32(
        weights=weights_dict['vit_b_32'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def vit_b_32(pretrain=True):
    return torchvision.models.vit_b_32(
        weights=weights_dict['vit_b_32'] if pretrain else None)


@SURROGATE_REGISTRY.register()
def swin_b(pretrain=True):
    return torchvision.models.swin_b(
        weights=weights_dict['swin_b'] if pretrain else None)
