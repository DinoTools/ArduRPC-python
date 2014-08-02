#!/usr/bin/env python
import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "ardurpc", "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],

    description=about["__summary__"],
    long_description=long_description,
    license=about["__license__"],
    url=about["__uri__"],

    zip_safe=False,
    author=about["__author__"],
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
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    package_dir={
        "ardurpc": "ardurpc"
    },
    include_package_data=True,
    package_data = {
        '': ["LICENSE", "README.md"],
    }
)
