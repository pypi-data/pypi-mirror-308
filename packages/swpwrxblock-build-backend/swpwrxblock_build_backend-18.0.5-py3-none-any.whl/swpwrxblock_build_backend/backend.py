# -*- coding: utf-8 -*-
# pylint: disable=C0415,C0115,missing-function-docstring
"""
Custom [PEP-518](https://peps.python.org/pep-0518/) build backend for setuptools
to copy assets before building the package. This is a part of the build system
for the SWPWRXBlock XBlock.

How this works:
1. The backend is specified in pyproject.toms of https://github.com/QueriumCorp/swpwrxblock/
2. the build system will call the backend to build the package:

        [build-system]
        requires = ["setuptools", "wheel", "swpwrxblock-build-backend"]
        build-backend = "swpwrxblock_build_backend.backend"

   where "swpwrxblock-build-backend" is this repo published to PyPi,
   and where "swpwrxblock_build_backend.backend" is the path to this file.
"""

# built-in stuff
import sys

# 3rd-party stuff
from setuptools import build_meta

# our stuff
from .collect_reactapp import copy_assets
from .utils import logger

logger("backend.py import successful")
logger("sys.path=" + str(sys.path))


class SWPWRXBlockBuildBackend:
    """
    Custom build backend for setuptools to copy assets before building the package.

    Note that as of the initial publication of this package, PIP-518 did not
    yet support class-based build backends, so this includes a simpler
    module-based implementation as well. See defs below this class definition.
    """

    def __init__(self):
        logger("SWPWRXBlockBuildBackend.__init__() called")

    def build_wheel(
        self, wheel_directory, config_settings=None, metadata_directory=None
    ):
        logger("SWPWRXBlockBuildBackend.build_wheel() called")
        retval = build_meta.build_wheel(
            wheel_directory, config_settings, metadata_directory
        )
        logger(
            "SWPWRXBlockBuildBackend.build_wheel() parent build_wheel() complete: "
            + str(retval)
        )
        copy_assets()
        return retval

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
        return self._prepare_metadata_for_build_wheel(
            metadata_directory, config_settings
        )

    def _prepare_metadata_for_build_wheel(
        self, metadata_directory, config_settings=None
    ):
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
