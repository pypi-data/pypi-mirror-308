import torch
from torch import nn


class EnhancedBN(nn.Module):
    def __init__(self, nc: int, sty_nc: int = 3, sty_nhidden: int = 128):
        super(EnhancedBN, self).__init__()
        self.bn = nn.BatchNorm2d(nc)
        self.mapping = nn.Conv2d(
            in_channels=sty_nc,
            out_channels=sty_nhidden,
            kernel_size=3,
            padding=1,
            stride=1,
        )
        self.gamma = nn.Conv2d(
            in_channels=sty_nhidden,
            out_channels=nc,
            kernel_size=3,
            padding=1,
            stride=1,
        )
        self.beta = nn.Conv2d(
            in_channels=sty_nhidden,
            out_channels=nc,
            kernel_size=3,
            padding=1,
            stride=1,
        )
        self.init_weight()

    def init_weight(self):
        nn.init.kaiming_normal_(self.mapping.weight)
        nn.init.kaiming_normal_(self.gamma.weight)
        nn.init.kaiming_normal_(self.beta.weight)

    def forward(self, base, sty):
        bn = self.bn(base)
        sty_resized = torch.nn.functional.interpolate(
            sty, size=bn.size()[2:], mode='bilinear'
        )
        actv = torch.nn.functional.relu(self.mapping(sty_resized))
        # style injection
        bn = bn * (1 + self.gamma(actv)) + self.beta(actv)
        return bn


class ResidualBlock(nn.Module):
    def __init__(self, num_filters):
        super(ResidualBlock, self).__init__()
        self.block1 = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(
                in_channels=num_filters,
                out_channels=num_filters,
                kernel_size=3,
                stride=1,
                padding=0,
                bias=False,
            ),
        )
        self.bn1 = EnhancedBN(num_filters)
        self.block2 = nn.Sequential(
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
        )
        self.bn2 = EnhancedBN(num_filters)

    def forward(self, x, sty):
        residual = self.block1(x)
        residual = self.bn1(residual, sty)
        residual = self.block2(residual)
        residual = self.bn2(residual, sty)
        return x + residual


ngf = 64


class ResNetGenerator(nn.Module):
    def __init__(self):
        super(ResNetGenerator, self).__init__()
        self.block1 = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(3, ngf, kernel_size=7, padding=0, bias=False),
        )
        self.bn1 = EnhancedBN(ngf)
        # Input size = 3, n, n
        self.block2 = nn.Sequential(
            nn.Conv2d(
                ngf, ngf * 2, kernel_size=3, stride=2, padding=1, bias=False
            ),
        )
        self.bn2 = EnhancedBN(ngf * 2)
        # Input size = 3, n/2, n/2
        self.block3 = nn.Sequential(
            nn.Conv2d(
                ngf * 2,
                ngf * 4,
                kernel_size=3,
                stride=2,
                padding=1,
                bias=False,
            ),
        )
        self.bn3 = EnhancedBN(ngf * 4)
        # Input size = 3, n/4, n/4
        # Residual Blocks: 6
        self.resblock1 = ResidualBlock(ngf * 4)
        self.resblock2 = ResidualBlock(ngf * 4)
        self.resblock3 = ResidualBlock(ngf * 4)
        self.resblock4 = ResidualBlock(ngf * 4)
        self.resblock5 = ResidualBlock(ngf * 4)
        self.resblock6 = ResidualBlock(ngf * 4)
        # Input size = 3, n/4, n/4
        self.upsampl1 = nn.ConvTranspose2d(
            ngf * 4,
            ngf * 2,
            kernel_size=3,
            stride=2,
            padding=1,
            output_padding=1,
            bias=False,
        )
        self.ubn1 = EnhancedBN(ngf * 2)
        # Input size = 3, n/2, n/2
        self.upsampl2 = nn.ConvTranspose2d(
            ngf * 2,
            ngf,
            kernel_size=3,
            stride=2,
            padding=1,
            output_padding=1,
            bias=False,
        )
        self.ubn2 = EnhancedBN(ngf)
        # Input size = 3, n, n
        self.blockf = nn.Sequential(
            nn.ReflectionPad2d(3), nn.Conv2d(ngf, 3, kernel_size=7, padding=0)
        )

    def forward(self, input, sty):
        x = self.block1(input)
        x = self.bn1(x, sty)
        x = torch.nn.functional.relu(x)
        x = self.block2(x)
        x = self.bn2(x, sty)
        x = torch.nn.functional.relu(x)
        x = self.block3(x)
        x = self.bn3(x, sty)
        x = torch.nn.functional.relu(x)
        # =============================
        x = self.resblock1(x, sty)
        x = self.resblock2(x, sty)
        x = self.resblock3(x, sty)
        x = self.resblock4(x, sty)
        x = self.resblock5(x, sty)
        x = self.resblock6(x, sty)
        # =============================
        x = self.upsampl1(x)
        x = self.ubn1(x, sty)
        x = torch.nn.functional.relu(x)
        x = self.upsampl2(x)
        x = self.ubn2(x, sty)
        x = torch.nn.functional.relu(x)
        x = self.blockf(x)
        return (torch.tanh(x) + 1) / 2


AIMGenerator = ResNetGenerator
