import os

# Load version
version_path = os.path.join(os.path.dirname(__file__), "version.txt")
with open(version_path, "r") as version_file:
    __version__ = version_file.read().strip()

lib_version_path = os.path.join(os.path.dirname(__file__), "lib_version.txt")
with open(lib_version_path, "r") as lib_version_file:
    __lib_version__ = lib_version_file.read().strip()

from .uparma import UParma
from .uparma import UParmaDict
