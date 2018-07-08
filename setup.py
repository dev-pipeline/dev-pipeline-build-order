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
            'build-order = devpipeline_buildorder.build_order:_BUILD_ORDER_COMMAND'
        ],

        'devpipeline.build_order.methods': [
            'dot = devpipeline_buildorder.dot:_DOT_TOOL',
            'graph = devpipeline_buildorder.dot:_GRAPH_TOOL',
            'layers = devpipeline_buildorder.dot:_LAYERS_TOOL',
            'list = devpipeline_buildorder:_LIST_TOOL'
        ]
    },

    author="Stephen Newell",
    description="build-order command for dev-pipeline",
    license="BSD-2"
)
