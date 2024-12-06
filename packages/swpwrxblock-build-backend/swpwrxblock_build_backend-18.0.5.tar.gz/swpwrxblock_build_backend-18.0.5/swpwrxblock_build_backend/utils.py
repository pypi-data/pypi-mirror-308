# -*- coding: utf-8 -*-
"""Install utilities for the stepwise-power-xblock XBlock."""

import os

from .const import DEBUG_MODE

print("DEBUG: swpwrxblock_build_backend.utils import successful")


def logger(msg: str):
    """
    Print a message to the console.
    """
    if not DEBUG_MODE:
        return

    prefix = "DEBUG: swpwrxblock-build-backend"
    print(prefix + " - " + msg)


def validate_path(path):
    """
    Check if a path exists, and raise an exception if it does not.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"copy_assets() path not found: {path}")
    logger("validate_path() validated: " + path)
