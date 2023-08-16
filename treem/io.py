"""SWC data format defintion and services."""

import json

import numpy as np


class SWC():  # pylint: disable=too-few-public-methods
    """Definitions of the data format."""
    TYPES = (SOMA, AXON, DEND, APIC) = range(1, 5)
    COLS = (I, T, X, Y, Z, R, P) = range(7)  # noqa: E741
    XY = slice(2, 4)
    XZ = slice(2, 5, 2)
    YZ = slice(3, 5)
    XYZ = slice(2, 5)
    XYZR = slice(2, 6)
    RADII = slice(5, 6)


class TreemEncoder(json.JSONEncoder):
    """Extended JSONEncoder to serialize treem objects."""
    def default(self, obj):  # pylint: disable=arguments-differ
        if hasattr(obj, 'tolist'): 
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def load_swc(source):
    """Reads data from SWC file."""
    return np.loadtxt(source)


def save_swc(target, data):
    """Writes data to SWC file."""
    fmt = '%d %d %g %g %g %g %d'
    return np.savetxt(target, data, fmt=fmt)
