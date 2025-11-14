"""Implementation of CLI modify command."""

import math

from itertools import chain

import numpy as np

from treem.morph import Morph
from treem.io import SWC
from treem.utils.geom import rotation


def _scale_radii(morph, nodes, scale_radius):
    """Scales radii."""
    scale = np.abs(scale_radius)
    for node in nodes:
        sec = list(node.section())
        radii = morph.radii(sec)  # NOSONAR (S1481) "Necessary for in-place NumPy modification"
        radii *= scale


def _scale_coords(morph, nodes, scale_coords):
    """Scales X,Y,Z coordinates."""
    scale = np.abs(scale_coords)
    for node in nodes:
        sec = list(node.section())
        head = sec[0].coord().copy()
        tail = sec[-1].coord().copy()
        coords = morph.coords(sec)  # NOSONAR (S1481) "Necessary for in-place NumPy modification"
        coords *= np.array(scale)
        shift = head - sec[0].coord()
        coords += shift
        for child in sec[-1].siblings:
            shift = sec[-1].coord() - tail
            morph.translate(shift, child)


def _jitter_coords(morph, nodes, jitter, rng, args):
    """Adds random jitter to X,Y,Z coordinates."""
    for node in nodes:
        sec = list(node.section())
        if len(sec) > 1:
            head = sec[0].coord().copy()
            tail = sec[-1].coord().copy()
            length = morph.length(sec[1:])
            coords = morph.coords(sec)
            if not args.sec:
                rnd = rng.uniform(-1, 1, np.shape(coords))
                coords += jitter * rnd
            else:
                xlen = 0
                rnd = rng.uniform(-1, 1, 3)
                for node in sec:
                    xlen += node.length()
                    vec = jitter * rnd * xlen / length
                    morph.move(vec, node)
            scale = length / morph.length(sec[1:])
            coords *= scale
            shift = head - sec[0].coord()
            coords += shift
            for child in sec[-1].siblings:
                shift = sec[-1].coord() - tail
                morph.translate(shift, child)


def _twist_branches(morph, nodes, twist, rng):
    """Rotates branches by random angle."""
    for node in nodes:
        axis = node.coord() - node.parent.coord()
        angle = twist * rng.uniform(-1, 1) * math.pi / 180
        morph.rotate(axis, angle, node)


def _stretch_sections(morph, nodes, stretch):
    """Straighten sections by relative factor."""
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
                coord += vdir * np.linalg.norm(coord - head) * stretch
            scale = length / morph.length(sec[1:])
            coords *= scale
            shift = head - sec[0].coord()
            coords += shift
            for child in sec[-1].siblings:
                shift = sec[-1].coord() - tail
                morph.translate(shift, child)


def _smooth_sections(morph, nodes, smooth):
    """Smooth sections iteratively by low-pass filtering."""
    for node in nodes:
        sec = list(node.section())
        if len(sec) > 2:
            head = sec[0].coord().copy()
            tail = sec[-1].coord().copy()
            length = morph.length(sec[1:])
            coords = morph.coords(sec)
            for _ in range(smooth):
                for secnode in sec[-1::-1]:
                    coord = secnode.coord()
                    coord += secnode.parent.coord()
                scale = length / morph.length(sec[1:])
                coords *= scale
                shift = head - sec[0].coord()
                coords += shift
            for child in sec[-1].siblings:
                shift = sec[-1].coord() - tail
                morph.translate(shift, child)


def _swap_branches(morph, node1, node2):
    """Swap two branches."""
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



def _prune_branches(morph, nodes, args):
    """Prune branches if structure is not changed."""
    if not args.swap:
        for node in nodes:
            morph.prune(node)


def _collect_nodes(morph, args):
    """Collects nodes by given ids, default to section start nodes."""
    if args.ids:
        nodes = filter(lambda x: x.ident() in args.ids, morph.root.walk())
    else:
        sections = chain.from_iterable(x.sections() for x in morph.stems())
        nodes = chain(sec[0] for sec in sections)
    return nodes


def _filter_attr(nodes, args):
    """Selects nodes by given attributes."""
    types = args.type if args.type else SWC.TYPES
    nodes = filter(lambda x: x.type() in types, nodes)
    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)
    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)
    return list(nodes)


def _set_random_generator(args):
    """Initialize random generator."""
    if args.seed:
        rng = np.random.default_rng(seed=args.seed)
    else:
        rng = np.random.default_rng(0)
    return rng


def modify(args):
    """Modifies selected parts of morphology reconstruction."""
    morph = Morph(args.file)
    rng = _set_random_generator(args)

    # collect nodes to operate on
    nodes = _collect_nodes(morph, args)
    nodes = _filter_attr(nodes, args)

    # manipulate morphology at specified nodes
    if args.scale_radius:
        _scale_radii(morph, nodes, args.scale_radius)

    if args.scale:
        _scale_coords(morph, nodes, args.scale)

    if args.jitter:
        _jitter_coords(morph, nodes, args.jitter, rng, args)

    if args.twist:
        _twist_branches(morph, nodes, args.twist, rng)

    if args.stretch:
        _stretch_sections(morph, nodes, args.stretch)

    if args.smooth:
        _smooth_sections(morph, nodes, args.smooth)

    if args.swap:
        rng.shuffle(nodes)
        node1, node2 = nodes[:2]
        _swap_branches(morph, node1, node2)

    if args.prune:
        _prune_branches(morph, nodes, args)

    # renumber nodes in restructured morphology
    if args.prune or args.swap:
        morph = Morph(data=morph.data)

    morph.save(args.out)
