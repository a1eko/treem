"""Testing module geom."""

import os

import numpy as np
from numpy.testing import assert_array_almost_equal

from treem import Morph
from treem.utils.geom import (
    fibonacci_sphere,
    repair_branch,
    rotation,
    rotation_matrix,
    sample,
)


def test_fibonacci_sphere():
    """Tests fibonacci_sphere."""
    N = 1000
    points = fibonacci_sphere(npoints=N)
    expected_shape = (N, 3)
    assert points.shape == expected_shape
    magnitudes_squared = np.sum(points**2, axis=1)
    expected_magnitudes = np.ones(N)
    assert_array_almost_equal(magnitudes_squared, expected_magnitudes, decimal=10)


def test_tree_rotation():
    """Tests 3D rotation."""
    vec = [1, 0, 0]
    result_vec, result_scalar = rotation(vec, vec)
    expected_vec = np.array([0., 0.70710678, -0.70710678])
    expected_scalar = 0.0
    assert np.allclose(result_vec, expected_vec)
    assert np.isclose(result_scalar, expected_scalar)
    vecx = [1, 0, 0]
    vecy = [0, 1, 0]
    vecz = [0, 0, 1]
    result_vec, result_scalar = rotation(vecx, vecy)
    expected_vec = np.array(vecz)
    expected_scalar = np.pi / 2
    assert np.allclose(result_vec, expected_vec)
    assert np.isclose(result_scalar, expected_scalar)


def test_rotation_matrix():
    """Tests rotation_matrix."""
    vec = [1, 0, 0]
    rot = np.pi / 2
    result_matrix = rotation_matrix(vec, rot)
    expected_matrix = np.array([[1., 0., 0.],
                                [0., 0., -1.],
                                [0., 1., 0.]])
    assert np.allclose(result_matrix, expected_matrix)


def test_sample():
    """Tests point interpolation."""
    points = np.array([[0, 0, 0, 1],
                       [3, 0, 0, 1]])
    expected_sample = np.array([[0., 0., 0., 1.],
                                [1., 0., 0., 1.],
                                [2., 0., 0., 1.],
                                [3., 0., 0., 1.]])
    result_sample = sample(points, 4)
    assert np.allclose(result_sample, expected_sample)


def test_repair_branch():
    """Tests repair_branch."""
    os.chdir(os.path.dirname(__file__) + '/data')
    cmorph = Morph('pass_simple_branch.swc')
    rmorph = Morph('pass_simple_branch_2.swc')
    cut = [node for node in cmorph.root.walk() if node.ident()==13][0]
    rep = [node for node in rmorph.root.walk() if node.ident()==12][0]
    res = repair_branch(cmorph, cut, rmorph, rep)
    assert res == 1
    assert [node.ident() for node in cmorph.root.walk()] == list(range(1, 17))


def test_repair_branch_short():
    """Tests repair_branch, short section."""
    os.chdir(os.path.dirname(__file__) + '/data')
    cmorph = Morph('pass_simple_branch.swc')
    rmorph = Morph('pass_zjump.swc')
    cut = [node for node in cmorph.root.walk() if node.ident()==13][0]
    rep = [node for node in rmorph.root.walk() if node.ident()==10][0]
    res = repair_branch(cmorph, cut, rmorph, rep, keep_radii=True)
    assert res == 1
    assert [node.ident() for node in cmorph.root.walk()] == list(range(1, 17))
