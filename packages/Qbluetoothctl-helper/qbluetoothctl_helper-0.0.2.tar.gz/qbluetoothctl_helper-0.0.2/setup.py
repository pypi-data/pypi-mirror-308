#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is a python install script written for pyIMU python package.
# pip3 install --upgrade setuptools wheel Cython build twine
#
# python3 setup.py build_ext --inplace
# python3 setup.py bdist
# python3 setup.py sdist bdist_wheel
# twine upload --repository testpypi dist/*
# twine upload dist/*
#
# python3 setup.py bdist_wheel
# pip3 install -e . # -e makes symlinks to the source folder and allows editing the source code without having to reinstall the package
#

import io
import os
from setuptools import setup, find_packages
# Uncomment if you intend to use Cython:
# from Cython.Build import cythonize

here = os.path.abspath(os.path.dirname(__file__))

# Load long description from README.md
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# If you intend to use Cython for building modules:
# cython_modules_path = here  # If files are in the current directory
# module_files = [os.path.join(cython_modules_path, f) for f in os.listdir(cython_modules_path) if f.endswith(".py")]
# excluded_files = [os.path.join(cython_modules_path, "__init__.py")]

setup(
    name='Qbluetoothctl_helper',
    version='0.0.2',
    description="Python bluetoothctl helper for QT.",
    url='https://github.com/uutzinger/Qbluetoothctl_helper',
    author='Urs Utzinger',
    author_email='uutzinger@gmail.com',
    # Uncomment if you use Cython and adjust accordingly:
    # ext_modules=cythonize(module_files, exclude=excluded_files, compiler_directives=dict(language_level="3")),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='bluetooth, bluetoothctl, Qt, pyQt',
    packages=find_packages(),  # Use this if your modules are in packages; otherwise, specify modules directly.
    py_modules=['Qbluetoothctl_helper'],
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'pyqt5': ['PyQt5>=5.15'],
        'pyqt6': ['PyQt6>=6.0'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)