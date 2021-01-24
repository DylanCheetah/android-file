"""A patch to provide reasonable external storage support on Android API 29+."""

import builtins
import os

from jnius import autoclass


#Globals
#===============================================================================
__version__ = "1.0.0"
__author__ = "Eric Snyder"
__license__ = "MIT"

_activity = autoclass("org.kivy.android.PythonActivity").mActivity
_external_storage_dir = _activity.getExternalFilesDir(None)
JavaFile = autoclass("java.io.File")
JavaFileInputStream = autoclass("java.io.FileInputStream")
JavaFileOutputStream = autoclass("java.io.FileOutputStream")


#Classes
#===============================================================================
class AndroidFile(object):
    """A class that encapsulates a native Android file."""
    def __init__(self, filename, mode = "r"):
        """Setup this Android file."""
        #First, open the appropriate file
        if filename.startswith("/external/"):
            filename = filename.replace("/external/", "")
            self._file = JavaFile(_external_storage_dir, filename)

        else:
            raise IOError("Failed to open Android file.")

        #Next, open the correct type of file stream
        if mode == "r":
            self._stream = JavaFileInputStream(self._file)

        elif mode == "w":
            self._stream = JavaFileOutputStream(self._file)

        else:
            raise IOError("Failed to open Android file stream.")

    def __del__(self):
        """Close this Android file."""
        self.close()

    def __enter__(self):
        """Setup context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context manager."""
        self.close()

    def close(self):
        """Close this Android file."""
        self._stream.close()

    def read(self, n = -1):
        """Read up to n bytes from this file. If n is -1, read all remaining
        bytes.
        """
        if n == -1:
            n = self._file.length()

        data = bytearray(n)
        self._stream.read(data)
        return bytes(data)

    def write(self, data):
        """Write the given data to this file."""
        if isinstance(data, str):
            data = data.encode("ascii")

        data = bytearray(data)
        self._stream.write(data)

    def flush(self):
        """Write buffered data to this file and empty the buffer."""
        self._stream.flush()


#Functions
#===============================================================================
def open(filename, mode = "r"):
    """Open the given file in the given mode."""
    if filename.startswith("/external/"):
        return AndroidFile(filename, mode)

    else:
        return builtins.open(filename, mode)


def listdir(dir):
    """List the files inside the given dir."""
    if dir.startswith("/external/"):
        dir = dir.replace("/external/", "")
        file = JavaFile(_external_storage_dir, dir)
        return file.list()

    else:
        return os.listdir(dir)