"""Testing module geom."""

import numpy as np

from treem.utils.geom import rotation


def test_tree_rotation():
    """Tests 3D rotation."""
    vec = [1, 0, 0]
    assert np.allclose(rotation(vec, vec)[0],
                       np.array([0., 0.70710678, -0.70710678]))
    assert rotation(vec, vec)[1] == 0.0
