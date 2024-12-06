#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Union

from setuptools import find_packages, setup

try:
    sys.path.append(str(Path(__file__).parent / 'src'))
    import gat
except ImportError:
    print('Please install aim_attack package')
    sys.exit(1)


def read(path: Union[str, Path]) -> str:
    with open(path, 'r') as f:
        return f.read()


setup(name='pygat',
      version=gat.version(),
      description='GAT: Generative Attack Toolbox',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      author='Terry Li',
      url='https://terrytengli.com/gat/',
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License'
      ],
      python_requires='>=3.10',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['tqdm', 'tabulate', 'torch', 'torchvision'],
      include_package_data=True)
