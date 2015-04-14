#!/usr/bin/env python
import sys

from setuptools import setup, find_packages


if sys.version_info < (2, 7):
    raise Exception("This package requires Python 2.7 or higher.")


def read_release_version():
    """Read the version from the file ``RELEASE-VERSION``"""
    try:
        with open("RELEASE-VERSION", "r") as f:
            version = f.readlines()[0]
            return version.strip()
    except IOError:
        return "0.0.0-development"

setup(
    name='Philly Fire API',
    description='An API for Philadelphia Fire Department data',
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'Sphinx==1.1.3',
    ],
    long_description='An API for Philadelphia Fire Department data',
    dependency_links=['http://pypi.colo.lair/simple/'],
    version=read_release_version(),
    author='Amber Heilman',
    author_email='amber.l.heilma@gmail.com',
    entry_points={}
)
