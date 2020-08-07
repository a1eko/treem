"""Implementation of CLI repair command."""

import math

from itertools import chain

import numpy as np

from treem import Morph, SWC
from treem.utils.geom import repair_branch, sample, norm, rotation


def repair(args):
    """Corrects morphology reconstruction at the given nodes."""
    # pylint: disable=invalid-name
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=cell-var-from-loop
    # pylint: disable=expression-not-assigned
    vprint = print if args.verbose else lambda *a, **k: None
    morph = Morph(args.file)
    err = 0

    if args.center:
        morph.data[:, SWC.XYZ] -= morph.root.coord()

    if args.translate:
        morph.data[:, SWC.XYZ] += np.array(args.translate)

    if args.rotate:
        morph.rotate([1, 0, 0], args.rotate[0]/180*math.pi)
        morph.rotate([0, 1, 0], args.rotate[1]/180*math.pi)
        morph.rotate([0, 0, 1], args.rotate[2]/180*math.pi)

    if args.shrink_xy:
        scale = np.array([args.shrink_xy, args.shrink_xy, 1])
        origin = morph.root.coord().copy()
        for stem in morph.stems():
            for node in stem.walk():
                coord = node.coord()
                coord *= scale
        shift = origin - morph.root.coord()
        morph.translate(shift)

    if args.shrink:
        if args.bottom_up:
            bottom = max(x.coord()[2] for x in morph.root.walk())
        else:
            bottom = min(x.coord()[2] for x in morph.root.walk())
        for node in morph.root.walk():
            z = node.coord()[2]
            z = bottom + args.shrink * (z - bottom)
            node.v[SWC.Z] = z

    if args.zjump:
        nodes = [x for x in morph.root.walk() if x.ident() in args.zjump]
        for node in nodes:
            jump = node.parent.coord()[2] - node.coord()[2]
            if args.zjump_mode == 'align':
                shift = [0, 0, jump]
                morph.translate(shift, node)
            elif args.zjump_mode == 'split':
                shift = [0, 0, jump/2]
                jump_sec = list(node.section())
                for split_node in jump_sec[:int(len(jump_sec)/2)]:
                    morph.move(shift, split_node)
            elif args.zjump_mode == 'tilt':
                parent = node.parent
                dist = max(norm(parent.coord()-jump_node.coord())
                           for jump_node in node.leaves())
                leng = max(norm(node.coord()-jump_node.coord())
                           for jump_node in node.leaves())
                leaf = [jump_node for jump_node in node.leaves()
                        if norm(node.coord()-jump_node.coord()) == leng][0]
                vdir = leaf.coord() - node.parent.coord()
                shift = [0, 0, jump*leng/dist]
                morph.translate(shift, node)
                udir = leaf.coord() - node.coord()
                axis, angle = rotation(udir, vdir)
                morph.rotate(axis, angle, node)
            elif args.zjump_mode == 'join':
                parent = node.parent
                dist = max(norm(parent.coord()-jump_node.coord())
                           for jump_node in node.leaves())
                leng = max(norm(node.coord()-jump_node.coord())
                           for jump_node in node.leaves())
                leaf = [jump_node for jump_node in node.leaves()
                        if norm(node.coord()-jump_node.coord()) == leng][0]
                vdir = leaf.coord() - node.parent.coord()
                shift = [0, 0, jump*leng/dist]
                morph.translate(shift, node)
                udir = leaf.coord() - node.coord()
                axis, angle = rotation(udir, vdir)
                morph.rotate(axis, angle, node)
                start = list(node.section(reverse=True))[-1].parent
                dist = max(norm(start.coord()-jump_node.coord())
                           for jump_node in node.leaves())
                leng = morph.length(node.parent.section(reverse=True))
                vdir = leaf.coord() - start.coord()
                shift = [0, 0, -jump*leng/dist]
                morph.translate(shift, node.parent)
                udir = leaf.coord() - node.coord()
                axis, angle = rotation(udir, vdir)
                morph.rotate(axis, angle, node)

    if args.pool:
        pool = [Morph(f) for f in args.pool]

    if args.diam:
        nodes = [x for x in morph.root.walk() if x.ident() in args.diam]
        if args.pool:
            types = {x.type() for x in nodes}
        if args.diam_mode == 'joint':
            for node in nodes:
                r = 0
                if node.parent.type() != SWC.SOMA:
                    r += node.parent.radius()
                    r /= 2
                if not node.is_fork():
                    r += node.siblings[0].radius()
                    r /= 2
                if r:
                    node.v[SWC.R] = r
                else:
                    vprint(f'diam in node {node.ident()} not repaired')
                    err += 1
        elif args.diam_mode == 'sec':
            for node in nodes:
                sec = list(node.section(reverse=True))
                sec = list(sec[-1].section())
                r = morph.radii(sec).mean()
                node.v[SWC.R] = r
        elif args.diam_mode == 'order':
            for node in nodes:
                point_type = node.type()
                order = node.order()
                if args.pool:
                    radii = [m.radii(sec).mean() for m in pool
                             for sec in m.root.sections()
                             if sec[0].type() in types
                             and sec[0].order() == order]
                    if radii:
                        r = np.mean(radii)
                        node.v[SWC.R] = r
                    else:
                        vprint(f'diam in node {node.ident()} (order {order}) '
                               f'not repaired')
                        err += 1
                else:
                    r = np.array([morph.radii(sec).mean()
                                  for sec in morph.root.sections()
                                  if sec[0].type() == point_type
                                  and sec[0].order() == order]).mean()
                    node.v[SWC.R] = r
        elif args.diam_mode == 'breadth':
            for node in nodes:
                point_type = node.type()
                breadth = node.breadth()
                if args.pool:
                    radii = [m.radii(sec).mean() for m in pool
                             for sec in m.root.sections()
                             if sec[0].type() in types
                             and sec[0].breadth() == breadth]
                    if radii:
                        r = np.mean(radii)
                        node.v[SWC.R] = r
                    else:
                        vprint(f'diam in node {node.ident()} '
                               f'(breadth {breadth}) not repaired')
                        err += 1
                else:
                    r = np.array([morph.radii(sec).mean()
                                  for sec in morph.root.sections()
                                  if sec[0].type() == point_type
                                  and sec[0].breadth() == breadth]).mean()
                    node.v[SWC.R] = r

    if args.seed:
        np.random.seed(args.seed)

    if args.cut:  # pylint: disable=too-many-nested-blocks
        types = {x.type() for x in morph.root.walk() if x.ident() in args.cut}
        for point_type in types:
            intact_branches = dict()
            if args.pool:
                for rec in pool:
                    sections = filter(lambda x: x[0].type() == point_type,
                                      rec.root.sections())
                    nodes = chain(x[0] for x in sections)
                    for node in nodes:
                        order = node.order()
                        if order not in intact_branches:
                            intact_branches[order] = list()
                        intact_branches[order].append((rec, node))
            else:
                sections = filter(lambda x: x[0].type() == point_type,
                                  morph.root.sections())
                nodes = chain(x[0] for x in sections)

                def is_intact(tree, cuts):
                    leaves = [x.ident() for x in tree.leaves()]
                    return set(leaves).isdisjoint(cuts)

                nodes = filter(lambda x: is_intact(x, args.cut), nodes)
                for node in nodes:
                    order = node.order()
                    if order not in intact_branches:
                        intact_branches[order] = list()
                    intact_branches[order].append((morph, node))

            nodes = [x for x in morph.root.walk() if x.type() == point_type
                     and x.ident() in args.cut]
            for node in nodes:
                order = node.order()
                vprint(f'repairing node {node.ident()} (order {order})',
                       end=' ')
                if order in intact_branches:
                    idx = np.random.choice(len(intact_branches[order]))
                    rec, rep = intact_branches[order][idx]
                    vprint(f'using {rep.ident()} (order {order}) ...', end=' ')
                    done = repair_branch(morph, node, rec, rep,
                                         force=args.force_repair)
                    err += 1 if not done else 0
                    vprint('done') if done else vprint('not repaired')
                elif order - 1 in intact_branches:
                    idx = np.random.choice(len(intact_branches[order-1]))
                    rec, rep = intact_branches[order-1][idx]
                    vprint(f'using {rep.ident()} (order {order-1}) ...',
                           end=' ')
                    done = repair_branch(morph, node, rec, rep,
                                         force=args.force_repair)
                    err += 1 if not done else 0
                    vprint('done') if done else vprint('not repaired')
                elif args.force_repair:
                    if intact_branches:
                        order = np.random.choice(list(intact_branches.keys()))
                        idx = np.random.choice(len(intact_branches[order]))
                        rec, rep = intact_branches[order][idx]
                        vprint(f'using {rep.ident()} (order {order}) ...',
                               end=' ')
                        done = repair_branch(morph, node, rec, rep, force=True)
                        err += 1 if not done else 0
                        vprint('done') if done else vprint('not repaired')
                    else:
                        err += 1
                        vprint('... no intact branches, not repaired')
                else:
                    err += 1
                    vprint('... not repaired')

    if args.delete and not args.cut:
        nodes = [x for x in morph.root.walk() if x.ident() in args.delete]
        for node in nodes:
            morph.delete(node)

    if args.delete or args.cut:
        morph = Morph(data=morph.data)

    if args.res:
        ident = 1
        data = list()
        idmap = {-1: -1}
        for sec in filter(lambda x: x[0].type() == SWC.SOMA,
                          morph.root.sections()):
            for node in sec:
                v = node.v.copy()
                i, p = v[SWC.I].astype(int), v[SWC.P].astype(int)
                v[SWC.I], v[SWC.P] = ident, idmap[p]
                idmap[i] = ident
                data.append(v)
                ident += 1
        for sec in filter(lambda x: x[0].type() in
                          set(SWC.TYPES).difference((SWC.SOMA,)),
                          morph.root.sections()):
            length = morph.length(sec)
            points = morph.points(sec)
            # pylint: disable=unsubscriptable-object
            points = np.insert(points, 0, sec[0].parent.v[SWC.XYZR], axis=0)
            points = sample(points, np.rint(length/args.res).astype(int))
            points = points[1:]
            start = True
            for ident, point in enumerate(points, ident):
                x, y, z, r = point
                pid = idmap[sec[0].parent_ident()] if start else ident - 1
                v = np.array([ident, sec[0].type(), x, y, z, r, pid])
                start = False if start else start
                data.append(v)
            idmap[sec[-1].v[SWC.I]] = ident
            ident += 1
        morph = Morph(data=data)

    morph.save(args.out)
    return err
