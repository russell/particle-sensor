# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='particle-sensor',
    version='0.1.0',
    description='',
    long_description=README,
    author='Russell Sim',
    author_email='russell.sim@gmail.com',
    url='https://github.com/russell/particle-sensor',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
