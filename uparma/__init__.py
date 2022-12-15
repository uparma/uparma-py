import os
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = None

# Version
__version_str__ = str(__version__)

lib_version_path = os.path.join(os.path.dirname(__file__), "lib_version.txt")
with open(lib_version_path, "r") as lib_version_file:
    __lib_version__ = lib_version_file.read().strip()

from .uparma import UParma
from .uparma import UParmaDict
