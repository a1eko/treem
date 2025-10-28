"""Implementation of CLI modify command."""

import math

from itertools import chain

import numpy as np

from treem.morph import Morph
from treem.io import SWC
from treem.utils.geom import rotation


def modify(args):
    """Modifies selected parts of morphology reconstruction."""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    morph = Morph(args.file)
    if args.ids:
        nodes = filter(lambda x: x.ident() in args.ids, morph.root.walk())
    else:
        sections = chain.from_iterable(x.sections() for x in morph.stems())
        nodes = chain(x[0] for x in sections)
    types = args.type if args.type else SWC.TYPES
    nodes = filter(lambda x: x.type() in types, nodes)
    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)
    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)
    nodes = list(nodes)

    if args.scale_radius:
        scale_radius = np.abs(args.scale_radius)
        for node in nodes:
            sec = list(node.section())
            radii = morph.radii(sec)
            #radii *= scale_radius
            radii = radii * scale_radius

    if args.scale:
        scale = np.abs(args.scale)
        for node in nodes:
            sec = list(node.section())
            head = sec[0].coord().copy()
            tail = sec[-1].coord().copy()
            coords = morph.coords(sec)
            coords *= np.array(scale)
            shift = head - sec[0].coord()
            coords += shift
            for child in sec[-1].siblings:
                shift = sec[-1].coord() - tail
                morph.translate(shift, child)

    if args.seed:
        np.random.seed(args.seed)

    if args.jitter:
        for node in nodes:
            sec = list(node.section())
            if len(sec) > 1:
                head = sec[0].coord().copy()
                tail = sec[-1].coord().copy()
                length = morph.length(sec[1:])
                coords = morph.coords(sec)
                if not args.sec:
                    rnd = np.random.uniform(-1, 1, np.shape(coords))
                    coords += args.jitter * rnd
                else:
                    xlen = 0
                    rnd = np.random.uniform(-1, 1, 3)
                    for node in sec:
                        xlen += node.length()
                        vec = args.jitter * rnd * xlen / length
                        morph.move(vec, node)
                scale_jitter = length / morph.length(sec[1:])
                coords *= scale_jitter
                shift = head - sec[0].coord()
                coords += shift
                for child in sec[-1].siblings:
                    shift = sec[-1].coord() - tail
                    morph.translate(shift, child)

    if args.twist:
        for node in nodes:
            axis = node.coord() - node.parent.coord()
            angle = args.twist * np.random.uniform(-1, 1) * math.pi / 180
            morph.rotate(axis, angle, node)

    if args.stretch:
        for node in nodes:
            sec = list(node.section())
            if len(sec) > 1:
                head = sec[0].coord().copy()
                tail = sec[-1].coord().copy()
                length = morph.length(sec[1:])
                coords = morph.coords(sec)
                vdir = coords.mean(axis=0) - head
                vdir /= np.linalg.norm(vdir)
                for secnode in sec[1:]:
                    coord = secnode.coord()
                    coord += vdir * np.linalg.norm(coord - head) * args.stretch
                scale_stretch = length / morph.length(sec[1:])
                coords *= scale_stretch
                shift = head - sec[0].coord()
                coords += shift
                for child in sec[-1].siblings:
                    shift = sec[-1].coord() - tail
                    morph.translate(shift, child)

    if args.smooth:
        for node in nodes:
            sec = list(node.section())
            if len(sec) > 2:
                head = sec[0].coord().copy()
                tail = sec[-1].coord().copy()
                length = morph.length(sec[1:])
                coords = morph.coords(sec)
                for _ in range(args.smooth):
                    for secnode in sec[-1::-1]:
                        coord = secnode.coord()
                        coord += secnode.parent.coord()
                    scale_smooth = length / morph.length(sec[1:])
                    coords *= scale_smooth
                    shift = head - sec[0].coord()
                    coords += shift
                for child in sec[-1].siblings:
                    shift = sec[-1].coord() - tail
                    morph.translate(shift, child)

    if args.swap:
        np.random.shuffle(nodes)
        # swap 2 nodes at a time
        for node1, node2 in zip(nodes[:1], nodes[1:]):
            parent1 = node1.parent
            parent2 = node2.parent
            dir1 = node1.coord() - parent1.coord()
            dir2 = node2.coord() - parent2.coord()
            tree1 = morph.copy(node1)
            tree2 = morph.copy(node2)
            coord1 = tree1.root.coord().copy()
            coord2 = tree2.root.coord().copy()
            tree1.translate(coord2 - coord1)
            axis, angle = rotation(dir1, dir2)
            tree1.rotate(axis, angle)
            tree2.translate(coord1 - coord2)
            axis, angle = rotation(dir2, dir1)
            tree2.rotate(axis, angle)
            morph.graft(tree1, parent2)
            morph.graft(tree2, parent1)
            morph.prune(node1)
            morph.prune(node2)

    if args.prune and not args.swap:
        for node in nodes:
            morph.prune(node)

    if args.prune or args.swap:
        morph = Morph(data=morph.data)

    morph.save(args.out)
