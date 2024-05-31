# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='SpeachToSpeach',
    version='0.1.0',
    description="",
    author="Tadiello Sébastien",
    author_email="sebastientadiello@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    # test_suite='test',
)