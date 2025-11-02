"""Implementation of CLI find command."""

import numpy as np

from treem.morph import Morph
from treem.io import SWC
from treem.utils.geom import fibonacci_sphere
from treem.utils.geom import rotation_matrix
from treem.utils.geom import rotation


Z_COORD_INDEX = 2


def _filter_by_comparison(nodes, args, attr_name, attr_accessor):
    """
    Apply a filter based on a comparison operation ('gt', 'lt', 'eq').

    :param attr_name: The name of the attribute in args (e.g., 'diam', 'length').
    :param attr_accessor: A function (node -> value) to get the attribute value.
    """
    attr_value = getattr(args, attr_name)
    if attr_value is None:
        return nodes
    comparator = args.compare
    if comparator == 'gt':
        nodes = filter(lambda x: attr_accessor(x) > attr_value, nodes)
    elif comparator == 'lt':
        nodes = filter(lambda x: attr_accessor(x) < attr_value, nodes)
    elif comparator == 'eq':
        nodes = filter(lambda x: attr_accessor(x) == attr_value, nodes)
    return nodes


def _get_z_jump(node):
    """Calculate the absolute Z-difference from parent, handling root node."""
    if node.is_root():
        return 0  # root node has no jump
    return abs((node.parent.coord() - node.coord())[Z_COORD_INDEX])


def _apply_simple_cut(nodes, morph, args):
    """Apply top-down or bottom-up Z-slice cut filter."""
    coord_accessor = lambda x: x.coord()[Z_COORD_INDEX]
    nodes = filter(lambda x: x.is_leaf(), nodes)
    node_walker = morph.root.walk()
    if not args.bottom_up:
        # upper cut
        zcut = max(coord_accessor(x) for x in node_walker)
        nodes = filter(lambda x: coord_accessor(x) > zcut - args.cut, nodes)
    else:
        # bottom cut
        zcut = min(coord_accessor(x) for x in node_walker)
        nodes = filter(lambda x: coord_accessor(x) < zcut + args.cut, nodes)
    return nodes


def _find_optimal_cuts(nodes, morph, args):
    """Find arbitrary cut plane by using Fibonacci sphere rotations."""
    node_list = list(nodes)
    points = fibonacci_sphere(args.cut_iter)
    ztip = np.array([x.v for x in morph.root.leaves()])
    zdir = (0, 0, 1)
    found_cuts = []
    for vdir in points:
        vtip = ztip.copy()
        axis, angle = rotation(zdir, vdir)
        rotm = rotation_matrix(axis, angle)
        vtip[:, SWC.XYZ] = np.dot(rotm, vtip[:, SWC.XYZ].T).T
        zmax = vtip[:, SWC.Z].max()
        cuts = [int(v[SWC.I]) for v in vtip if zmax - v[SWC.Z] < args.cut]
        found_cuts.append(cuts)
    max_cuts = max(len(x) for x in found_cuts)
    final_cuts = next(cuts for cuts in found_cuts if len(cuts) == max_cuts)
    return filter(lambda x: x.ident() in final_cuts, node_list)


def _apply_stem_filter(nodes):
    """Collect unique stem nodes."""
    stems = set()
    for node in nodes:
        # walk reverse up the tree to find all unique stem nodes for this branch
        stem_nodes = (x for x in node.walk(reverse=True) if x.is_stem() and x.type() != SWC.SOMA)
        stems.update(stem_nodes)
    return list(stems)


def find(args):
    """Locates single nodes in morphology reconstruction."""
    morph = Morph(args.file)
    types = args.type if args.type else SWC.TYPES
    nodes = filter(lambda x: x.type() in types, morph.root.walk())

    # simple ID and attribute filters
    if args.nodes:
        nodes = filter(lambda x: x.ident() in args.nodes, nodes)
    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)
    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)
    if args.degree:
        nodes = filter(lambda x: x.degree() in args.degree, nodes)

    # comparative filters
    nodes = _filter_by_comparison(nodes, args, 'diam', lambda x: x.diam())
    nodes = _filter_by_comparison(nodes, args, 'length', lambda x: x.length())
    nodes = _filter_by_comparison(nodes, args, 'dist', lambda x: x.dist(morph.root.coord()))
    nodes = _filter_by_comparison(nodes, args, 'slice', lambda x: x.coord()[Z_COORD_INDEX])
    nodes = _filter_by_comparison(nodes, args, 'jump', _get_z_jump)

    # cut logic
    if args.cut:
        if not args.cut_find:
            nodes = _apply_simple_cut(nodes, morph, args)
        else:
            nodes = _find_optimal_cuts(nodes, morph, args)

    # structural filters
    if args.sec:
        # keep only nodes whose parent is a fork or root (start of a section)
        nodes = filter(lambda x: x.parent.is_fork() or x.parent.is_root(), nodes)

    if args.stem:
        nodes = _apply_stem_filter(nodes)

    # output
    for node in nodes:
        print(node.ident(), end=' ')
    print()
