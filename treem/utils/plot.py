"""Plotting utilities."""

import numpy as np

from treem.io import SWC

# pylint: disable=invalid-name


def plot_tree(ax, tree, data, **kwargs):
    """Plots entire branch.

    Args:
        ax: matplotlib axes object.
        tree (treem.Node): branch start node.
        data (NumPy ndarray): raw data of morphology Morph.
        kwargs: arguments for matplotlib plot().
    """
    # pylint: disable=too-many-locals
    for sec in tree.sections():
        first = sec[0].ident() - 1
        last = sec[-1].ident()
        block = slice(first, last)
        x, y, z = data[block, SWC.XYZ].T
        ax.plot(x, y, z, **kwargs)
    for bif in tree.forks():
        b = bif.coord()
        for child in bif.siblings:
            c = child.coord()
            a = np.array([b, c])
            x, y, z = a.T  # pylint: disable=unpacking-non-sequence
            ax.plot(x, y, z, **kwargs)


def plot_section(ax, tree, data, **kwargs):
    """Plots single section.

    Args:
        ax: matplotlib axes object.
        tree (treem.Node): branch start node.
        data (NumPy ndarray): raw data of morphology Morph.
        kwargs: arguments for matplotlib plot().
    """
    for sec in tree.sections():
        first = sec[0].ident() - 1
        last = sec[-1].ident()
        block = slice(first, last)
        x, y, z = data[block, SWC.XYZ].T
        ax.plot(x, y, z, **kwargs)
        break


def plot_neuron(ax, morph, types=SWC.TYPES, colors=None, linewidth=1):
    """Plots neuron morphology.

    Args:
        ax: matplotlib axes object.
        morph (treem.Morph): neuron morphology.
        types (int iterable): point types to be displayed.
        colors (dict): colors for point types ({pt: colspec}).
        linewidth (int): line width.
    """
    # pylint: disable=unpacking-non-sequence
    colors = colors if colors else {t: f'C{t}' for t in types}
    r = morph.root.coord()
    for stem in morph.stems():
        if stem.type() in types:
            x, y, z = np.array([r, stem.coord()]).T
            ax.plot(x, y, z, c=colors[stem.type()], lw=linewidth)
            plot_tree(ax, stem, morph.data, c=colors[stem.type()],
                      lw=linewidth)
    if SWC.SOMA in types:
        soma_points = morph.data[np.where(morph.data[:, SWC.T] == SWC.SOMA)]
        x, y, z = soma_points[:, SWC.XYZ].T
        ax.plot(x, y, z, linestyle='', marker='o', markersize=10,
                c=colors[SWC.SOMA], alpha=0.25)
    x, y, z = r
    ax.plot([x], [y], [z], linestyle='', marker='o', markersize=5,
            color='black')


def plot_points(ax, morph, ids, types=SWC.TYPES, show_id=False, markersize=6):
    """Plots marker points.

    Args:
        ax: matplotlib axes object.
        morph (treem.Morph): neuron morphology.
        ids (int iterable): list of node IDs.
        types (int iterable): point types to display.
    """
    # pylint: disable=too-many-arguments
    points = np.array([morph.data[x - 1] for x in ids
                       if morph.data[x - 1][SWC.T] in types])
    x, y, z = points[:, SWC.XYZ].T
    ax.plot(x, y, z, linestyle='', marker='.', markersize=markersize)
    if show_id:
        for point in points:
            x, y, z = point[SWC.XYZ]
            i = point[SWC.I].astype(int)
            ax.text3D(x, y, z, f'  {i}')
