# Code is copied from
# github.com/Alibaba-AAIG/Beyond-ImageNet-Attack:generator.py@863b7
import torch
from torch import nn


class ResidualBlock(nn.Module):
    def __init__(self, num_filters):
        super(ResidualBlock, self).__init__()
        self.block = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(
                in_channels=num_filters,
                out_channels=num_filters,
                kernel_size=3,
                stride=1,
                padding=0,
                bias=False,
            ),
            nn.BatchNorm2d(num_filters),
            nn.ReLU(True),
            nn.Dropout(0.5),
            nn.ReflectionPad2d(1),
            nn.Conv2d(
                in_channels=num_filters,
                out_channels=num_filters,
                kernel_size=3,
                stride=1,
                padding=0,
                bias=False,
            ),
            nn.BatchNorm2d(num_filters),
        )

    def forward(self, x):
        residual = self.block(x)
        return x + residual


ngf = 64


class ResNetGenerator(nn.Module):
    """
    https://github.com/Alibaba-AAIG/Beyond-ImageNet-Attack/blob/863b758ee4f4a6d3d4e7777c5f94f457fa449f73/generator.py#L14

    Test Case:
    >>> netG = ResNetGenerator()
    >>> test_sample = torch.rand(1, 3, 224, 224)
    >>> print("Generator output:", netG(test_sample).size())
    >>> print(
    >>>     "Generator parameters:",
    >>>     sum(p.numel() for p in netG.parameters() if p.requires_grad),
    >>> )
    """

    def __init__(self, inception=False):
        super(ResNetGenerator, self).__init__()
        self.inception = inception
        self.block1 = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(3, ngf, kernel_size=7, padding=0, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
        )
        # output: (ngf) x (n) x (n)
        self.block2 = nn.Sequential(
            nn.Conv2d(
                ngf, ngf * 2, kernel_size=3, stride=2, padding=1, bias=False
            ),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
        )
        # output: (ngf*2) x (n/2) x (n/2)
        self.block3 = nn.Sequential(
            nn.Conv2d(
                ngf * 2,
                ngf * 4,
                kernel_size=3,
                stride=2,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
        )
        # output: (ngf*4) x (n/4) x (n/4)
        self.resblock1 = ResidualBlock(ngf * 4)
        self.resblock2 = ResidualBlock(ngf * 4)
        self.resblock3 = ResidualBlock(ngf * 4)
        self.resblock4 = ResidualBlock(ngf * 4)
        self.resblock5 = ResidualBlock(ngf * 4)
        self.resblock6 = ResidualBlock(ngf * 4)
        # output: (ngf*4) x (n/4) x (n/4)
        self.upsampl1 = nn.Sequential(
            nn.ConvTranspose2d(
                ngf * 4,
                ngf * 2,
                kernel_size=3,
                stride=2,
                padding=1,
                output_padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
        )
        # output: (ngf*2) x (n/2) x (n/2)
        self.upsampl2 = nn.Sequential(
            nn.ConvTranspose2d(
                ngf * 2,
                ngf,
                kernel_size=3,
                stride=2,
                padding=1,
                output_padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
        )
        # output: (ngf) x (n) x (n)
        self.blockf = nn.Sequential(
            nn.ReflectionPad2d(3), nn.Conv2d(ngf, 3, kernel_size=7, padding=0)
        )
        self.crop = nn.ConstantPad2d((0, -1, -1, 0), 0)

    def forward(self, input):
        x = self.block1(input)
        x = self.block2(x)
        x = self.block3(x)
        x = self.resblock1(x)
        x = self.resblock2(x)
        x = self.resblock3(x)
        x = self.resblock4(x)
        x = self.resblock5(x)
        x = self.resblock6(x)
        x = self.upsampl1(x)
        x = self.upsampl2(x)
        x = self.blockf(x)
        if self.inception:
            x = self.crop(x)
        return (torch.tanh(x) + 1) / 2


CDAGenerator = ResNetGenerator
