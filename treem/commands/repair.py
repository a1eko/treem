"""Implementation of CLI repair command."""

import math

from itertools import chain

import numpy as np

from treem import Morph, SWC
from treem.utils.geom import repair_branch, sample, norm, rotation


SKIP = 'not repaired'


def _correct_shrink_xy(morph, args):
    """Corrects for shrinkage in X,Y plane."""
    scale = np.array([args.shrink_xy, args.shrink_xy, 1])
    origin = morph.root.coord().copy()
    for node in morph.root.walk():
        coord = node.coord()  # NOSONAR (S1481) "Necessary for in-place NumPy modification"
        coord *= scale
    shift = origin - morph.root.coord()
    morph.translate(shift)


def _correct_shrink_z(morph, args):
    """Corrects for shrinkage in Z axis."""
    if args.bottom_up:
        bottom = max(x.coord()[2] for x in morph.root.walk())
    else:
        bottom = min(x.coord()[2] for x in morph.root.walk())
    for node in morph.root.walk():
        z = node.coord()[2]
        z = bottom + args.shrink * (z - bottom)
        node.v[SWC.Z] = z


def _fix_by_tilt(morph, node, jump):
    """Corrects z-jump by tilting the section."""
    parent = node.parent
    dist = max(norm(parent.coord() - jump_node.coord())
               for jump_node in node.leaves())
    leng = max(norm(node.coord() - jump_node.coord())
               for jump_node in node.leaves())
    leaf = [jump_node for jump_node in node.leaves()
            if norm(node.coord() - jump_node.coord()) == leng][0]
    vdir = leaf.coord() - node.parent.coord()
    shift = [0, 0, jump * leng / dist]
    morph.translate(shift, node)
    udir = leaf.coord() - node.coord()
    axis, angle = rotation(udir, vdir)
    morph.rotate(axis, angle, node)
    return leaf


def _correct_zjumps(morph, nodes, args):
    """Corrects for discontinuties along Z axis in given nodes."""
    for node in nodes:
        jump = node.parent.coord()[2] - node.coord()[2]
        if args.zjump_mode == 'align':
            shift = [0, 0, jump]
            morph.translate(shift, node)
        elif args.zjump_mode == 'split':
            shift = [0, 0, jump / 2]
            jump_sec = list(node.section())
            for split_node in jump_sec[:int(len(jump_sec) / 2)]:
                morph.move(shift, split_node)
        elif args.zjump_mode == 'tilt':
            _ = _fix_by_tilt(morph, node, jump)
        elif args.zjump_mode == 'join':
            leaf = _fix_by_tilt(morph, node, jump)
            start = list(node.section(reverse=True))[-1].parent
            dist = max(norm(start.coord() - jump_node.coord())
                       for jump_node in node.leaves())
            leng = morph.length(node.parent.section(reverse=True))
            vdir = leaf.coord() - start.coord()
            shift = [0, 0, -jump * leng / dist]
            morph.translate(shift, node.parent)
            udir = leaf.coord() - node.coord()
            axis, angle = rotation(udir, vdir)
            morph.rotate(axis, angle, node)


def _fix_by_joint(nodes, vprint):
    """Set diameter to mean value of neighbour nodes."""
    err = 0
    for node in nodes:
        r = []
        if node.parent.type() != SWC.SOMA:
            r.append(node.parent.radius())
        if not node.is_fork() and not node.is_leaf():
            r.append(node.siblings[0].radius())
        if r:
            node.v[SWC.R] = np.mean(r)
        else:
            vprint(f'diam in node {node.ident()} {SKIP}')
            err += 1
    return err


def _fix_by_sec(morph, nodes):
    """Set diameter to mean value of the section."""
    for node in nodes:
        sec = list(node.section(reverse=True))
        sec = list(sec[-1].section())
        r = morph.radii(sec).mean()
        node.v[SWC.R] = r


def _fix_by_order(morph, nodes, pool, types, vprint, args):
    """Set diameter to mean value of sections with the same topological order."""
    err = 0
    for node in nodes:
        point_type = node.type()
        order = node.order()
        if args.pool:
            radii = [m.radii(sec).mean() for m in pool
                     for sec in m.root.sections()
                     if sec[0].type() in types and sec[0].order() == order]
            if radii:
                r = np.mean(radii)
                node.v[SWC.R] = r
            else:
                vprint(f'diam in node {node.ident()} (order {order}) {SKIP}')
                err += 1
        else:
            r = np.array([morph.radii(sec).mean()
                          for sec in morph.root.sections()
                          if sec[0].type() == point_type and sec[0].order() == order]).mean()
            node.v[SWC.R] = r
    return err


def _fix_by_breadth(morph, nodes, pool, types, vprint, args):
    """Set diameter to mean value of sections with the same topological breadth."""
    err = 0
    for node in nodes:
        point_type = node.type()
        breadth = node.breadth()
        if args.pool:
            radii = [m.radii(sec).mean() for m in pool
                     for sec in m.root.sections()
                     if sec[0].type() in types and sec[0].breadth() == breadth]
            if radii:
                r = np.mean(radii)
                node.v[SWC.R] = r
            else:
                vprint(f'diam in node {node.ident()} (breadth {breadth}) {SKIP}')
                err += 1
        else:
            r = np.array([morph.radii(sec).mean()
                          for sec in morph.root.sections()
                          if sec[0].type() == point_type and sec[0].breadth() == breadth]).mean()
            node.v[SWC.R] = r
    return err


def _fix_by_value(nodes, args):
    """Set diameter to specified value."""
    for node in nodes:
        node.v[SWC.R] = args.diam_value / 2


def _correct_diameters(morph, nodes, pool, vprint, args):
    """Corrects diameters in given nodes."""
    types = None
    err = 0
    if args.pool:
        types = {x.type() for x in nodes}
    if args.diam_mode == 'joint':
        err += _fix_by_joint(nodes, vprint)
    elif args.diam_mode == 'sec':
        _fix_by_sec(morph, nodes)
    elif args.diam_mode == 'order':
        err += _fix_by_order(morph, nodes, pool, types, vprint, args)
    elif args.diam_mode == 'breadth':
        err += _fix_by_breadth(morph, nodes, pool, types, vprint, args)
    if args.diam_mode == 'value':
        _fix_by_value(nodes, args)
    return err


def _set_random_generator(args):
    """Initialize random generator."""
    if args.seed:
        rng = np.random.default_rng(seed=args.seed)
    else:
        rng = np.random.default_rng(0)
    return rng


def _is_intact(tree, cuts):
    leaves = [x.ident() for x in tree.leaves()]
    return set(leaves).isdisjoint(cuts)


def _delete_cut_branches(morph, cuts, vprint):
    """Deletes cut branches, resets cuts to corresponding stems. Returns updated morphology."""
    types = {x.type() for x in morph.root.walk() if x.ident() in cuts}
    stems = []
    for cut in cuts:
        stems.extend(x for x in filter(lambda x: x.is_stem() and x.type() != SWC.SOMA,
                                       morph.node(cut).walk(reverse=True))
                     if x not in stems)
    for node in stems:
        for child in node.siblings:
            morph.prune(child)
    vprint('renumbering nodes, old node ids are lost')
    morph = Morph(data=morph.data)
    cuts = {x.ident() for x in morph.root.siblings if x.is_leaf() and x.type() in types}
    vprint(f'reassigning cut points to {cuts}')
    return morph, cuts


def _graft_branches(morph, morig, graft_points, pool, vprint, rng, args):
        """Grafts branches onto soma."""
        point_type = args.graft_point_type
        intact_branches = []
        err = 0
        if args.pool:
            for rec in pool:
                sections = filter(lambda x: x[0].type() == point_type and x[0].order() == 1, rec.root.sections())
                nodes = chain(x[0] for x in sections)
                for node in nodes:
                    intact_branches.append((rec, node))
        else:
            sections = filter(lambda x: x[0].type() == point_type and x[0].order() == 1,
                              morig.root.sections())
            nodes = chain(x[0] for x in sections)

            nodes = filter(lambda x: _is_intact(x, args.cut), nodes)
            for node in nodes:
                intact_branches.append((morig, node))

        vprint('grafting branch on to a soma node', end=' ')
        nodes = [x for x in morph.root.walk() if x.ident() in graft_points]
        for node in nodes:
            vprint(f'{node.ident()}', end=' ')
            if intact_branches:
                idx = rng.choice(len(intact_branches))
                rec, rep = intact_branches[idx]
                morph.graft(rec.copy(rep), node)
                vprint('done')
            else:
                err += 1
                vprint('... no intact branches, not grafted')
        return err


def _make_intact_dict(morph, nodes):
    """Creates dictionary of non-damaged branches."""
    intact_branches = {}
    for node in nodes:
        order = node.order()
        if order not in intact_branches:
            intact_branches[order] = []
        intact_branches[order].append((morph, node))
    return intact_branches


def _collect_intact_branches(morig, pool, point_type, args):
        """Collects branches not containing cut points."""
        intact_branches = {}
        if args.pool:
            for rec in pool:
                sections = filter(lambda x, t=point_type: x[0].type() == t, rec.root.sections())
                nodes = chain(x[0] for x in sections)
                rec_branches = _make_intact_dict(rec, nodes)
                intact_branches.update(rec_branches)
        else:
            sections = filter(lambda x, t=point_type: x[0].type() == t, morig.root.sections())
            nodes = chain(x[0] for x in sections)
            nodes = filter(lambda x: _is_intact(x, args.cut), nodes)
            intact_branches = _make_intact_dict(morig, nodes)

        return intact_branches


def _repair_by_order(morph, intact_branches, node, order, vprint, rng, args):
        """Repair using branches of given topological order."""
        err = 0
        idx = rng.choice(len(intact_branches[order]))
        rec, rep = intact_branches[order][idx]
        vprint(f'using {rep.ident()} (order {order}) ...', end=' ')
        done = repair_branch(morph, node, rec, rep,
                             force=args.force_repair,
                             keep_radii=args.keep_radii)
        err += 1 if not done else 0
        vprint('done') if done else vprint(SKIP)
        return err


def _repair_cut_branches(morph, morig, cuts, pool, vprint, rng, args):
    """Repairs cut branches."""
    err = 0
    types = {x.type() for x in morph.root.walk() if x.ident() in cuts}
    for point_type in types:
        intact_branches = _collect_intact_branches(morig, pool, point_type, args)

        nodes = [x for x in morph.root.walk() if x.type() == point_type and x.ident() in cuts]
        for node in nodes:
            order = node.order()
            vprint(f'repairing node {node.ident()} (order {order})',
                   end=' ')
            if order in intact_branches:
                err += _repair_by_order(morph, intact_branches, node, order, vprint, rng, args)

            elif order - 1 in intact_branches:
                err += _repair_by_order(morph, intact_branches, node, order - 1, vprint, rng, args)

            elif args.force_repair:
                if intact_branches:
                    order = rng.choice(list(intact_branches.keys()))
                    err += _repair_by_order(morph, intact_branches, node, order, vprint, rng, args)
                else:
                    err += 1
                    vprint(f'... no intact branches, {SKIP}')
            else:
                err += 1
                vprint(f'... {SKIP}')
    return err


def _repair_neurites(morph, cuts, pool, vprint, rng, args):
    """Repairs cut neurites."""
    morig = morph.copy() if args.rotate and args.cut else morph
    err = 0
    if args.del_branch:
        morph, cuts = _delete_cut_branches(morph, cuts, vprint)
        graft_points = set()
        args.keep_radii = True
    else:
        graft_points = set(args.cut).difference(cuts)
    err += _repair_cut_branches(morph, morig, cuts, pool, vprint, rng, args)
    if graft_points:
        err += _graft_branches(morph, morig, graft_points, pool, vprint, rng, args)
    return err, morph


def _delete_branches(morph, idents):
    """Prunes branches and returns new morphology."""
    nodes = [x for x in morph.root.walk() if x.ident() in idents]
    for node in nodes:
        morph.delete(node)
    return Morph(data=morph.data)


def _resample(morph, res):
    """Samples neurites with new spatial resolution and returns new morphology."""
    ident = 1
    data = []
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
        parent_point = sec[0].parent.v[SWC.XYZR]
        # parent root: if sec[0].parent.is_root():
        # parent root:     parent_point[3] = sec[0].v[SWC.R]
        points = np.insert(points, 0, parent_point, axis=0)
        points = sample(points, np.ceil(length / res).astype(int))
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
    return Morph(data=np.array(data))



def _flip(morph, flip):
    """Flips morphology around root along specified axes."""
    center = morph.root.coord().copy()
    if 'x' in flip:
        morph.data[:, SWC.X] *= -1
    if 'y' in flip:
        morph.data[:, SWC.Y] *= -1
    if 'z' in flip:
        morph.data[:, SWC.Z] *= -1
    shift = morph.root.coord() - center
    morph.data[:, SWC.XYZ] -= shift


def repair(args):
    """Corrects morphology reconstruction at the given nodes."""
    vprint = print if args.verbose else lambda *a, **k: None
    morph = Morph(args.file)
    rng = _set_random_generator(args)
    pool = None
    err = 0

    if args.translate:
        morph.data[:, SWC.XYZ] += np.array(args.translate)

    if args.rotate:
        morph.rotate([1, 0, 0], args.rotate[0] / 180 * math.pi)
        morph.rotate([0, 1, 0], args.rotate[1] / 180 * math.pi)
        morph.rotate([0, 0, 1], args.rotate[2] / 180 * math.pi)

    if args.shrink_xy:
        _correct_shrink_xy(morph, args)

    if args.shrink:
        _correct_shrink_z(morph, args)

    if args.zjump:
        nodes = [x for x in morph.root.walk() if x.ident() in args.zjump]
        _correct_zjumps(morph, nodes, args)

    if args.pool:
        pool = [Morph(f) for f in args.pool]

    if args.diam:
        nodes = [x for x in morph.root.walk() if x.ident() in args.diam]
        err += _correct_diameters(morph, nodes, pool, vprint, args)

    if args.cut:
        cuts = {x for x in args.cut if morph.node(x).type() != SWC.SOMA}
        nerr, morph = _repair_neurites(morph, cuts, pool, vprint, rng, args)
        err += nerr
        morph = Morph(data=morph.data)

    if args.delete and not args.cut:
        morph = _delete_branches(morph, args.delete)

    if args.res:
        morph = _resample(morph, args.res)

    if args.flip:
        _flip(morph, args.flip)

    if args.center:
        morph.data[:, SWC.XYZ] -= morph.root.coord()

    morph.save(args.out)
    return err
