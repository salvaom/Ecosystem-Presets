#!/usr/bin/env python
from setuptools import setup, find_packages
import os

setup(
    name='Ecosystem-Presets',
    version='1.0.0',
    description='Preset extension for Ecosystem',
    url='https://github.com/salvaom/ecosystem-presets',
    author='Salvador Olmos Miralles',
    author_email='salvaom11@gmail.com',
    packages=find_packages(os.path.join(os.path.dirname(__file__), 'source')),
    package_dir={
        '': 'source'
    },
)
