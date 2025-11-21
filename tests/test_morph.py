"""Testing module morph."""

import numpy as np

from treem import Morph, Node


def test_node_str():
    """Tests for Node string representation."""
    node = Node(value=1)
    assert str(node) == '1'


def test_node_stem_leaf():
    """Tests for Node stem and leaf attributes."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 3, 1, 0, 0, 1, 1],
                                 [3, 3, 2, 0, 0, 1, 2]]))
    stem = [node for node in morph.root.walk() if not node.is_root()][0]
    leaf = [node for node in morph.root.walk() if not node.is_root()][-1]
    assert stem.is_stem()
    assert leaf.is_leaf()


def test_node_order():
    """Tests for Node order attribute."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 3, 1, 0, 0, 1, 1],
                                 [3, 3, 2, 0, 0, 1, 2],
                                 [4, 3, 1, 2, 0, 1, 2],
                                 ]))
    orders = [0, 1, 2, 2]
    assert [node.order() for node in morph.root.walk()] == orders


def test_node_point():
    """Tests for Node data point."""
    node = Node(value=np.array([1, 1, 0, 0, 0, 1, -1]))
    assert all(node.point() == np.array([0, 0, 0, 1]))


def test_node_dist():
    """Tests for Node distance to origin."""
    node = Node(value=np.array([1, 1, 1, 0, 0, 1, -1]))
    assert np.isclose(node.dist(), 1.0)


def test_morph_node():
    """Tests for Morph node lookup."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1]]))
    node = morph.node(1)
    assert node.ident() == 1


def test_morph_insert():
    """Tests for Morph node insertion."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 1, 0, 0, 0, 1, 1]]))
    new_node = Node(value=np.array([0, 1, 0, 0, 0, 1, 0]))
    morph.insert(new_node, morph.node(2))
    assert morph.node(2).ident() == 2
    assert morph.node(3).ident() == 3
    assert morph.root.size() == 3


def test_node_area():
    """Tests node area."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1], [2, 3, 1, 0, 0, 1, 1]]))
    node = list(morph.root.leaves())[0]
    area = np.pi * node.diam() * node.length()
    assert node.area() == area


def test_node_volume():
    """Tests node volume."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1], [2, 3, 1, 0, 0, 1, 1]]))
    node = list(morph.root.leaves())[0]
    volume = np.pi * node.radius()**2 * node.length()
    assert node.volume() == volume


def test_sec_radii():
    """Tests section radii."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 3, 1, 0, 0, 1, 1],
                                 [3, 3, 2, 0, 0, 2, 2]]))
    stem = list(morph.stems())[0]
    sec = list(stem.sections())[0]
    radii = [[1], [2]]
    assert morph.radii(sec).tolist() == radii


def test_sec_points():
    """Tests section points data."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 3, 1, 0, 0, 1, 1],
                                 [3, 3, 2, 0, 0, 2, 2]]))
    stem = list(morph.stems())[0]
    sec = list(stem.sections())[0]
    points = [[1, 0, 0, 1], [2, 0, 0, 2]]
    assert morph.points(sec).tolist() == points


def test_sec_area():
    """Tests section area."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 3, 1, 0, 0, 1, 1],
                                 [3, 3, 2, 0, 0, 1, 2]]))
    node = list(morph.root.leaves())[0]
    sec = list(node.sections())[0]
    assert np.isclose(morph.area(sec), node.area())


def test_sec_volume():
    """Tests section volume."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 3, 1, 0, 0, 1, 1],
                                 [3, 3, 2, 0, 0, 1, 2]]))
    node = list(morph.root.leaves())[0]
    sec = list(node.sections())[0]
    assert np.isclose(morph.volume(sec), node.volume())


def test_save(tmp_path):
    """Tests saving morphology to SWC file."""
    morph = Morph(data=np.array([[1, 1, 0, 0, 0, 1, -1],
                                 [2, 3, 1, 0, 0, 1, 1],
                                 [3, 3, 2, 0, 0, 1, 2]]))
    morph.save(tmp_path / 'test_treem.json')
