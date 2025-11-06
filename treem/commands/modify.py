"""Implementation of CLI modify command."""

import math

import numpy as np

from itertools import chain
from treem.morph import Morph
from treem.io import SWC
from treem.utils.geom import rotation


def _filter_nodes(morph, args):
    """Filters morphology nodes based on command-line arguments."""
    if args.ids:
        nodes = filter(lambda x: x.ident() in args.ids, morph.root.walk())
    else:
        # get the first node of every section in every stem
        sections = chain.from_iterable(x.sections() for x in morph.stems())
        nodes = chain(x[0] for x in sections)
    types = args.type if args.type else SWC.TYPES
    nodes = filter(lambda x: x.type() in types, nodes)
    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)
    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)
    return list(nodes)


def _scale_radius(morph, nodes, scale_radius):
    """Scales the radius of selected sections."""
    scale_radius = np.abs(scale_radius)
    for node in nodes:
        sec = list(node.section())
        radii = morph.radii(sec)
        radii = radii * scale_radius  # same as *=


def _scale_coords(morph, nodes, scale):
    """Scales the coordinates of selected sections."""
    scale = np.abs(scale)
    for node in nodes:
        sec = list(node.section())
        head = sec[0].coord().copy()
        tail = sec[-1].coord().copy()
        coords = morph.coords(sec)
        coords = coords * np.array(scale)  # same as *=
        shift = head - sec[0].coord()
        coords += shift
        for child in sec[-1].siblings:
            shift = sec[-1].coord() - tail
            morph.translate(shift, child)


def _jitter_nodes(morph, nodes, args, rng):
    """Applies jitter to selected sections."""
    for node in nodes:
        sec = list(node.section())
        if len(sec) > 1:
            head = sec[0].coord().copy()
            tail = sec[-1].coord().copy()
            length = morph.length(sec[1:])
            coords = morph.coords(sec)
            if not args.sec:
                rnd = rng.uniform(-1, 1, np.shape(coords))
                coords += args.jitter * rnd
            else:
                xlen = 0
                rnd = rng.uniform(-1, 1, 3)
                for secnode in sec:
                    xlen += secnode.length()
                    vec = args.jitter * rnd * xlen / length
                    morph.move(vec, secnode)
            scale_jitter = length / morph.length(sec[1:])
            coords *= scale_jitter
            shift = head - sec[0].coord()
            coords += shift
            for child in sec[-1].siblings:
                shift = sec[-1].coord() - tail
                morph.translate(shift, child)


def _twist_nodes(morph, nodes, twist_angle, rng):
    """Applies a twist rotation to selected nodes."""
    for node in nodes:
        # avoid issues if node is root (no parent)
        if node.parent:
            axis = node.coord() - node.parent.coord()
            angle = twist_angle * rng.uniform(-1, 1) * math.pi / 180
            morph.rotate(axis, angle, node)


def _stretch_nodes(morph, nodes, stretch_factor):
    """Stretches selected sections."""
    for node in nodes:
        sec = list(node.section())
        if len(sec) > 1:
            head = sec[0].coord().copy()
            tail = sec[-1].coord().copy()
            length = morph.length(sec[1:])
            coords = morph.coords(sec)
            # calculate mean direction vector
            vdir = coords.mean(axis=0) - head
            vdir /= np.linalg.norm(vdir)
            # stretch the nodes
            for secnode in sec[1:]:
                coord = secnode.coord()
                coord += vdir * np.linalg.norm(coord - head) * stretch_factor
            # rescale to original length and shift
            scale_stretch = length / morph.length(sec[1:])
            coords *= scale_stretch
            shift = head - sec[0].coord()
            coords += shift
            for child in sec[-1].siblings:
                shift = sec[-1].coord() - tail
                morph.translate(shift, child)


def _smooth_nodes(morph, nodes, smooth_iterations):
    """Smooths selected sections."""
    for node in nodes:
        sec = list(node.section())
        if len(sec) > 2:
            head = sec[0].coord().copy()
            tail = sec[-1].coord().copy()
            length = morph.length(sec[1:])
            coords = morph.coords(sec)
            for _ in range(smooth_iterations):
                for secnode in sec[-1::-1]:
                    # simple moving average: update coord based on parent
                    if secnode.parent: # ensure parent exists before accessing its coord
                        coord = secnode.coord()
                        coord = coord + secnode.parent.coord()  # same as +=
                # scale back to preserve the original length
                scale_smooth = length / morph.length(sec[1:])
                coords = coords * scale_smooth  # same as *=
                shift = head - sec[0].coord()
                coords += shift
            for child in sec[-1].siblings:
                shift = sec[-1].coord() - tail
                morph.translate(shift, child)


def _swap_nodes(morph, nodes, rng):
    """Swaps selected nodes and their subtrees."""
    rng.shuffle(nodes)
    # swap 2 nodes at a time
    #intended behavior: for node1, node2 in zip(nodes[::2], nodes[1::2]):
    # swap 2 first nodes from the list, ignore the rest
    for node1, node2 in zip(nodes[:1], nodes[1:]):
        parent1 = node1.parent
        parent2 = node2.parent
        dir1 = node1.coord() - parent1.coord()
        dir2 = node2.coord() - parent2.coord()

        # copy, translate, and rotate tree 1
        tree1 = morph.copy(node1)
        coord1 = tree1.root.coord().copy()
        coord2 = node2.coord() # use node2 coord as destination
        tree1.translate(coord2 - coord1)
        axis, angle = rotation(dir1, dir2)
        tree1.rotate(axis, angle)

        # copy, translate, and rotate tree 2
        tree2 = morph.copy(node2)
        coord1 = node1.coord() # use node1 coord as destination
        coord2 = tree2.root.coord().copy()
        tree2.translate(coord1 - coord2)
        axis, angle = rotation(dir2, dir1)
        tree2.rotate(axis, angle)

        # graft and prune
        morph.graft(tree1, parent2)
        morph.graft(tree2, parent1)
        morph.prune(node1)
        morph.prune(node2)


def modify(args):
    """Modifies selected parts of morphology reconstruction."""
    # load reconstruction file
    morph = Morph(args.file)

    # filter selected nodes
    nodes = _filter_nodes(morph, args)

    # set up random number generator
    rng = np.random.default_rng(seed=args.seed if args.seed is not None else 0)

    # perform modifications
    if args.scale_radius:
        _scale_radius(morph, nodes, args.scale_radius)

    if args.scale:
        _scale_coords(morph, nodes, args.scale)

    if args.jitter:
        _jitter_nodes(morph, nodes, args, rng)

    if args.twist:
        _twist_nodes(morph, nodes, args.twist, rng)

    if args.stretch:
        _stretch_nodes(morph, nodes, args.stretch)

    if args.smooth:
        _smooth_nodes(morph, nodes, args.smooth)

    # swap subtrees originating at given nodes
    if args.swap:
        _swap_nodes(morph, nodes, rng)

    # prune subtrees originating at given nodes
    if args.prune and not args.swap:
        for node in nodes:
            morph.prune(node)

    # re-initialize the morphology if pruning or swapping occurred
    if args.prune or args.swap:
        morph = Morph(data=morph.data)

    morph.save(args.out)
