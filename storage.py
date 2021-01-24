"""External storage utilities for Android API 29+."""

import builtins
import os

from jnius import autoclass


#Globals
#===============================================================================
__version__ = "1.0.0"
__author__ = "Eric Snyder"
__license__ = "MIT"

_activity = autoclass("org.kivy.android.PythonActivity").mActivity
_external_storage_path = _activity.getExternalFilesDir(None).getPath()


#Functions
#===============================================================================
def get_external_storage_path():
    """Returns the external storage path for the current app."""
    return _external_storage_path