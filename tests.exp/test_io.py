"""Testing module io."""

import json

import numpy as np

from treem.io import TreemEncoder


def test_io_encoder():
    """Tests JSON encoder."""
    data = [[1, 2, 3], np.array(range(4, 7)), {7, 8, 9}, 0, "a"]
    assert json.dumps(data, cls=TreemEncoder) ==\
        '[[1, 2, 3], [4, 5, 6], [8, 9, 7], 0, "a"]'
