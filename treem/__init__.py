"""Modules for processing tree-like morphology reconstructions."""

# ruff: noqa: F403

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("treem")
except PackageNotFoundError:
    __version__ = "unknown"


from treem.morph import *
from treem.tree import *
