"""Implementation of CLI find command."""

import numpy as np

from treem.morph import Morph
from treem.io import SWC
from treem.utils.geom import fibonacci_sphere
from treem.utils.geom import rotation_matrix
from treem.utils.geom import rotation


def find(args):
    """Locates single nodes in morphology reconstruction."""
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    morph = Morph(args.file)
    types = args.type if args.type else SWC.TYPES
    nodes = filter(lambda x: x.type() in types, morph.root.walk())

    if args.nodes:
        nodes = filter(lambda x: x.ident() in args.nodes, nodes)

    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)

    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)

    if args.degree:
        nodes = filter(lambda x: x.degree() in args.degree, nodes)

    if args.diam is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: x.diam() > args.diam, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: x.diam() < args.diam, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: x.diam() == args.diam, nodes)

    if args.length is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: x.length() > args.length, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: x.length() < args.length, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: x.length() == args.length, nodes)

    if args.dist is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: x.dist(morph.root.coord()) > args.dist, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: x.dist(morph.root.coord()) < args.dist, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: x.dist(morph.root.coord()) == args.dist, nodes)

    if args.slice is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: x.coord()[2] > args.slice, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: x.coord()[2] < args.slice, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: x.coord()[2] == args.slice, nodes)

    if args.jump is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: not x.is_root() and abs((x.parent.coord() - x.coord())[2]) > args.jump, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: not x.is_root() and abs((x.parent.coord() - x.coord())[2]) < args.jump, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: not x.is_root() and abs((x.parent.coord() - x.coord())[2]) == args.jump, nodes)

    if args.cut:
        nodes = filter(lambda x: x.is_leaf(), nodes)
        if not args.cut_find:
            if not args.bottom_up:
                zcut = max(x.coord()[2] for x in morph.root.walk())
                nodes = filter(lambda x: x.coord()[2] > zcut - args.cut, nodes)
            else:
                zcut = min(x.coord()[2] for x in morph.root.walk())
                nodes = filter(lambda x: x.coord()[2] < zcut + args.cut, nodes)
        else:
            found_cuts = []
            node_list = list(nodes)
            # node_ids = [x.ident() for x in node_list]
            points = fibonacci_sphere(args.cut_iter)
            ztip = np.array([x.v for x in morph.root.leaves()])
            zdir = (0, 0, 1)
            for vdir in points:
                vtip = ztip.copy()
                axis, angle = rotation(zdir, vdir)
                rotm = rotation_matrix(axis, angle)
                vtip[:, SWC.XYZ] = np.dot(rotm, vtip[:, SWC.XYZ].T).T
                zmax = vtip[:, SWC.Z].max()
                cuts = [int(v[SWC.I]) for v in vtip if zmax - v[SWC.Z] < args.cut]
                found_cuts.append(cuts)
            max_cuts = max(len(x) for x in found_cuts)
            for cuts in found_cuts:
                if len(cuts) == max_cuts:
                    break
            nodes = filter(lambda x: x.ident() in cuts, node_list)

    if args.sec:
        nodes = filter(lambda x: x.parent.is_fork() or x.parent.is_root(), nodes)

    if args.stem:
        stems = []
        for node in nodes:
            stems.extend(x for x in filter(lambda x: x.is_stem() and x.type() != SWC.SOMA, node.walk(reverse=True))
                         if x not in stems)
        nodes = stems

    for node in nodes:
        print(node.ident(), end=' ')
    print()
