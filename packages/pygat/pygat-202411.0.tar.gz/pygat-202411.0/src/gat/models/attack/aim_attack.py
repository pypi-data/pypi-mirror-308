from collections import OrderedDict
from pathlib import Path
from typing import Union

import torch

from .generator.aim import AIMGenerator


class AIMAttack:

    def __init__(self,
                 device: Union[str, torch.device],
                 epsilon: float = 16 / 255) -> None:
        if isinstance(device, str):
            device = torch.device(device)
        self.device = device
        self.adv_gen = AIMGenerator().to(device)
        self.set_mode('eval')
        self.epsilon = epsilon

    def load_ckpt(self, ckpt: Union[str, Path, OrderedDict]) -> None:
        if isinstance(ckpt, str):
            ckpt = Path(ckpt)
        if isinstance(ckpt, Path):
            if not ckpt.exists():
                raise FileNotFoundError(f'File not found: {ckpt}')
            ckpt = torch.load(ckpt, map_location=self.device)
        self.adv_gen.load_state_dict(ckpt)
        self.adv_gen.to(self.device)

    def save_ckpt(self, ckpt: Union[str, Path]) -> None:
        if isinstance(ckpt, str):
            ckpt = Path(ckpt)
        _adv_gen_cpu = self.adv_gen.to('cpu')
        torch.save(_adv_gen_cpu.state_dict(), ckpt)

    def get_params(self) -> torch.nn.Parameter:
        return self.adv_gen.parameters()

    def set_mode(self, mode: str) -> None:
        assert mode in ['train', 'eval']
        self.adv_gen.train() if mode == 'train' else self.adv_gen.eval()

    def __call__(self, x_nat, x_guid) -> torch.Tensor:
        x_adv = self.adv_gen(x_nat, x_guid)
        x_adv = torch.min(torch.max(x_adv, x_nat - self.epsilon),
                          x_nat + self.epsilon)
        torch.clamp_(x_adv, 0.0, 1.0)
        return x_adv
