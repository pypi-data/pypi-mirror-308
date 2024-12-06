# -*- coding: utf-8 -*-
# pylint: disable=C0415,C0115,missing-function-docstring
"""
Custom build backend for setuptools to copy assets before building the package.

How this works:
1. The backend is specified in pyproject.toms of https://github.com/QueriumCorp/swpwrxblock/
2. the build system will call the backend to build the package:

        [build-system]
        requires = ["setuptools", "wheel", "swpwrxblock-build-backend"]
        build-backend = "swpwrxblock_build_backend.backend"

   where "swpwrxblock-build-backend" is this repo published to PyPi,
   and where "swpwrxblock_build_backend.backend" is the path to this file.
"""

import sys

from .utils import logger

logger("backend.py import successful")
logger("sys.path=" + sys.path)


class SWPWRXBlockBuildBackend:
    """
    Custom build backend for setuptools to copy assets before building the package.
    """

    def __init__(self):
        logger("SWPWRXBlockBuildBackend.__init__() called")

    def build_wheel(
        self, wheel_directory, config_settings=None, metadata_directory=None
    ):
        print("SWPWRXBlockBuildBackend.build_wheel() called")
        self._copy_assets()
        from setuptools import build_meta

        return build_meta.build_wheel(
            wheel_directory, config_settings, metadata_directory
        )

    def get_requires_for_build_wheel(self, config_settings=None):
        logger("SWPWRXBlockBuildBackend.get_requires_for_build_wheel() called")
        return []

    def get_requires_for_build_sdist(self, config_settings=None):
        logger("SWPWRXBlockBuildBackend.get_requires_for_build_sdist() called")
        return []

    def prepare_metadata_for_build_wheel(
        self, metadata_directory, config_settings=None
    ):
        logger("SWPWRXBlockBuildBackend.prepare_metadata_for_build_wheel() called")
        self._copy_assets()
        return self._prepare_metadata_for_build_wheel(
            metadata_directory, config_settings
        )

    def _copy_assets(self):
        from .collect_reactapp import copy_assets

        logger("SWPWRXBlockBuildBackend._copy_assets() called")
        copy_assets()

    def _prepare_metadata_for_build_wheel(
        self, metadata_directory, config_settings=None
    ):
        from setuptools import build_meta

        return build_meta.prepare_metadata_for_build_wheel(
            metadata_directory, config_settings
        )


# Expose the backend class
def get_requires_for_build_wheel(config_settings=None):
    logger("backend.get_requires_for_build_wheel() called")
    return ["setuptools", "wheel"]


def get_requires_for_build_sdist(config_settings=None):
    logger("backend.get_requires_for_build_sdist() called")
    return ["setuptools"]


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    logger("backend.prepare_metadata_for_build_wheel() called")
    backend = get_backend()
    return backend.prepare_metadata_for_build_wheel(metadata_directory, config_settings)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    logger("backend.build_wheel() called")
    backend = get_backend()
    return backend.build_wheel(wheel_directory, config_settings, metadata_directory)


def get_backend():
    logger("backend.get_backend() called")
    return SWPWRXBlockBuildBackend()
