"""Testing module morph."""

import numpy as np

from treem import Node, Morph


def test_node_str():
    """Tests for Node string representation."""
    node = Node(value=1)
    assert str(node) == '1'


def test_node_point():
    """Tests for Node data point."""
    node = Node(value=np.array([1, 1, 0, 0, 0, 1, -1]))
    assert all(node.point() == np.array([0, 0, 0, 1]))


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
