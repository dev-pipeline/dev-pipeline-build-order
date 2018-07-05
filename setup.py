#!/usr/bin/python3

from setuptools import setup, find_packages

setup(
    name="dev-pipeline-build-order",
    version="0.2.0",
    package_dir={
        "": "lib"
    },
    packages=find_packages("lib"),

    install_requires=[
        'dev-pipeline-core >= 0.2.0'
    ],

    entry_points={
        'devpipeline.drivers': [
            'build-order = devpipeline_buildorder.build_order:main'
        ]
    },

    author="Stephen Newell",
    description="build-order command for dev-pipeline",
    license="BSD-2"
)
