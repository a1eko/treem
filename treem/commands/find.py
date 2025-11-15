"""Implementation of CLI find command."""

import numpy as np

from treem.io import SWC
from treem.morph import Morph
from treem.utils.geom import fibonacci_sphere, rotation, rotation_matrix


def _filter_by_comparison(nodes, getter_func, target_val, compare_op):
    """Encapsulates the repetitive comparison filtering logic."""
    if target_val is None:
        return nodes
    if compare_op == 'gt':
        return filter(lambda x: getter_func(x) > target_val, nodes)
    elif compare_op == 'lt':
        return filter(lambda x: getter_func(x) < target_val, nodes)
    elif compare_op == 'eq':
        return filter(lambda x: getter_func(x) == target_val, nodes)
    return nodes


def _handle_cut_logic(morph, args, nodes):
    """Handles the complex logic for locating cut nodes."""
    nodes = filter(lambda x: x.is_leaf(), nodes)
    if not args.cut_find:
        # simple Z-axis cut
        node_coords = [x.coord()[2] for x in morph.root.walk()]
        if not node_coords:
            return [] # No nodes, return empty
        if not args.bottom_up:
            zcut = max(node_coords)
            return filter(lambda x: x.coord()[2] > zcut - args.cut, nodes)
        else:
            zcut = min(node_coords)
            return filter(lambda x: x.coord()[2] < zcut + args.cut, nodes)
    else:
        # complex cut point logic (Fibonacci sphere projection)
        found_cuts = []
        node_list = list(nodes)
        points = fibonacci_sphere(args.cut_iter)
        ztip = np.array([x.v for x in morph.root.leaves()])
        zdir = np.array([0, 0, 1])
        for vdir in points:
            vtip = ztip.copy()
            axis, angle = rotation(zdir, vdir)
            rotm = rotation_matrix(axis, angle)
            # apply rotation to the XYZ coordinates
            vtip[:, SWC.XYZ] = np.dot(rotm, vtip[:, SWC.XYZ].T).T
            zmax = vtip[:, SWC.Z].max()
            cuts = [int(v[SWC.I]) for v in vtip if zmax - v[SWC.Z] < args.cut]
            found_cuts.append(cuts)
        if not found_cuts:
             return []
        max_cuts = max(len(x) for x in found_cuts)
        best_cuts = next(cuts for cuts in found_cuts if len(cuts) == max_cuts)
        return filter(lambda x: x.ident() in best_cuts, node_list)


def find(args):
    """Locates single nodes in morphology reconstruction."""
    morph = Morph(args.file)
    types = args.type if args.type else SWC.TYPES
    # initialize with all nodes of the correct type
    nodes = filter(lambda x: x.type() in types, morph.root.walk())

    # simple attribute filters
    if args.nodes:
        nodes = filter(lambda x: x.ident() in args.nodes, nodes)
    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)
    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)
    if args.degree:
        nodes = filter(lambda x: x.degree() in args.degree, nodes)

    # filters using comparison
    nodes = _filter_by_comparison(nodes, lambda x: x.diam(), args.diam, args.compare)
    nodes = _filter_by_comparison(nodes, lambda x: x.length(), args.length, args.compare)
    root_coord = morph.root.coord()
    nodes = _filter_by_comparison(nodes, lambda x: x.dist(root_coord), args.dist, args.compare)
    nodes = _filter_by_comparison(nodes, lambda x: x.coord()[2], args.slice, args.compare)

    def jump_getter(x):
        return abs((x.parent.coord() - x.coord())[2]) if not x.is_root() else -1

    nodes = _filter_by_comparison(nodes, jump_getter, args.jump, args.compare)

    # filter cut points
    if args.cut:
        nodes = _handle_cut_logic(morph, args, nodes)

    # filter section start nodes
    if args.sec:
        nodes = filter(lambda x: x.parent.is_fork() or x.parent.is_root(), nodes)

    # find stems in nodes and replace nodes
    if args.stem:
        stems = set()
        for node in nodes:
            stems.update(x for x in node.walk(reverse=True) if x.is_stem() and x.type() != SWC.SOMA)
        nodes = stems

    # console output
    for node in nodes:
        print(node.ident(), end=' ')
    print()
