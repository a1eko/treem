"""Testing CLI command view."""

import os

import matplotlib.pyplot as plt

from treem import Morph
from treem.utils.plot import plot_neuron, plot_points, plot_section


def test_plot_neuron(tmp_path):
    """Tests plot_neuron."""
    os.chdir(os.path.dirname(__file__) + '/data')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    morph = Morph('pass_simple_branch.swc')
    plot_neuron(ax, morph)


def test_plot_points(tmp_path):
    """Tests plot_points."""
    os.chdir(os.path.dirname(__file__) + '/data')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    morph = Morph('pass_simple_branch.swc')
    ids = [node.ident() for node in morph.root.walk()]
    plot_points(ax, morph, ids, show_id=True)


def test_plot_section(tmp_path):
    """Tests plot_neuron."""
    os.chdir(os.path.dirname(__file__) + '/data')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    morph = Morph('pass_simple_branch.swc')
    node = morph.root.siblings[0]
    plot_section(ax, node, morph.data)
