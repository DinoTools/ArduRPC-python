#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
import sys

import ardurpc

setup(
    name="ardurpc",
    version=ardurpc.__version__,
    license="LGPLv3",
    description="An extensible library to control microcontroller boards like Arduino using Python and the ArduRPC protocol",
    zip_safe=False,
    author="DinoTools.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3"
    ],
    #install_requires=[""],
    packages=find_packages(),
    package_dir={
        "ardurpc": "ardurpc"
    },
    include_package_data=True,
    package_data = {
        '': ["LICENSE", "README.md"],
    }
)
