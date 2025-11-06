"""Testing module geom."""

import numpy as np

from treem.utils.geom import rotation


def test_tree_rotation():
    """Tests 3D rotation."""
    vec = [1, 0, 0]
    result_vec, result_scalar = rotation(vec, vec)
    expected_vec = np.array([0., 0.70710678, -0.70710678])
    expected_scalar = 0.0
    assert np.allclose(result_vec, expected_vec)
    assert np.isclose(result_scalar, expected_scalar)
