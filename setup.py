#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c)
:license: MIT, see LICENSE for more details.
"""
import os
import sys

from setuptools import setup
from setuptools.command.install import install

# current version
VERSION = "0.0.13"


def readme():
    """print long description"""
    with open('README.rst') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="PySDDP",
    version=VERSION,
    description="PySDDP package",
    long_description=readme(),
    long_description_content_type='text/x-rst',
    url="https://github.com/AndreMarcato/PySDDP",
    author="Andre Marcato",
    author_email="andre.marcato@ufjf.edu.br",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords='pysddp',
    packages=["PySDDP"],
    py_modules=[],
    install_requires=["numpy", "matplotlib", "cvxopt", "pyswarm", "scipy", "typing", "pandas"],
    include_package_data=True,
    python_requires='>=3',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
