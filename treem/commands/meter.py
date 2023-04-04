"""Implementation of CLI meter command (experimental)."""

import os
import json
import math

import numpy as np
import multiprocessing as mp

from treem import Morph, SWC

from treem.io import TreemEncoder
from treem.utils.geom import norm


NSWCCOLS = len(SWC.COLS)
NXCOLS = 14
XCOLS = (DEGREE, ORDER, BREADTH, ASYM, BRANCH, TERM, DIST, PATH, 
         LENGTH, AREA, VOLUME, TOTLEN, TOTAREA, TOTVOL) = range(NSWCCOLS, NSWCCOLS + NXCOLS)
SECLEN = 3
CONTRAC = 4

ptmap = dict(zip(SWC.TYPES, ['soma', 'axon', 'dend', 'apic']))


def partition_asymmetry(breadths):
    """Computes partition asymmetry from breadths of two trees."""
    left, right = breadths[:2]
    asym = (abs(left - right) / (left + right - 2)) if left != right else 0.0
    return asym


def get_segdata(morphology, point_types):
    # FIXME process point_types only
    nrows = np.shape(morphology.data)[0]
    zeros = np.zeros((nrows, NXCOLS))
    segdata = np.append(morphology.data, zeros, axis=1)
    segdata = np.insert(segdata, 0, np.zeros(NSWCCOLS + NXCOLS), axis=0)
    center = morphology.root.coord()
    for stem in morphology.root.siblings:
        order = 1
        path = 0.0
        for node in stem.walk():
            ident = node.ident()
            length = node.length()
            area = node.area()
            volume = node.volume()
            if node.parent.is_fork() and node.parent != morphology.root:
                order += 1
            dist = np.linalg.norm(center - node.coord())
            path += length
            segdata[ident][DEGREE] = node.degree()
            segdata[ident][ORDER] = order
            segdata[ident][BREADTH] = 1
            segdata[ident][BRANCH] = 1 if node.is_fork() else 0
            segdata[ident][TERM] = 1 if node.is_leaf() else 0
            segdata[ident][DIST] = dist
            segdata[ident][PATH] = path
            segdata[ident][LENGTH] = length
            segdata[ident][AREA] = area
            segdata[ident][VOLUME] = volume
    for term in morphology.root.leaves():
        for node in term.walk(reverse=True):
            if not node.is_leaf():
                ident = node.ident()
                descent_ident = [x.ident() for x in node.siblings]
                descent_length = [x.length() for x in node.siblings]
                descent_area = [x.area() for x in node.siblings]
                descent_volume = [x.volume() for x in node.siblings]
                descent_breadth = [segdata[i][BREADTH] for i in descent_ident]
                descent_totlen = [segdata[i][TOTLEN] for i in descent_ident]
                descent_totarea = [segdata[i][TOTAREA] for i in descent_ident]
                descent_totvol = [segdata[i][TOTVOL] for i in descent_ident]
                breadth = sum(descent_breadth)
                totlen = sum(descent_totlen) + sum(descent_length)
                totarea = sum(descent_totarea) + sum(descent_area)
                totvol = sum(descent_totvol) + sum(descent_volume)
                segdata[ident][BREADTH] = breadth
                segdata[ident][TOTLEN] = totlen
                segdata[ident][TOTAREA] = totarea
                segdata[ident][TOTVOL] = totvol
            if node.is_fork() and not node.is_root():
                ident = node.ident()
                descent_ident = [x.ident() for x in node.siblings]
                descent_breadth = [segdata[i][BREADTH] for i in descent_ident]
                asym = partition_asymmetry(descent_breadth)
                segdata[ident][ASYM] = asym
            elif not node.is_leaf() and not node.is_root():
                ident = node.ident()
                child = node.siblings[0]
                descent_ident = child.ident()
                asym = segdata[descent_ident][ASYM]
                segdata[ident][ASYM] = asym
    return segdata[1:]


def get_secdata(morphology, point_types, full_mode=False):
    secdata = dict()
    for point_type in set(point_types).difference((SWC.SOMA,)):
        sdata = list()
        for sec in filter(lambda x: x[0].type() == point_type,
                          morphology.root.sections()):
            head = sec[0]
            tail = sec[-1]
            seclen = morphology.length(sec)
            chord = norm(tail.coord() - head.parent.coord())
            coords = morphology.coords(sec)
            xmin, ymin, zmin = np.min(coords, axis=0)
            xmax, ymax, zmax = np.max(coords, axis=0)
            if full_mode:
                sdata.append(
                    [tail.degree(), head.order(), tail.breadth(),
                     seclen, chord / seclen,
                     morphology.area(sec), morphology.volume(sec),
                     morphology.radii(sec).mean() * 2,
                     xmin, xmax, ymin, ymax, zmin, zmax])
            else:
                contrac = chord / seclen
                sdata.append([0, 0, 0, seclen, contrac, 
                              0, 0, 0, 0, 0, 0, 0, 0, 0])

        secdata[ptmap[point_type]] = sdata
    return secdata


def get_sholldata(morphology, point_types):
    pass


def get_morphometry(reconstruction, args):
    morph = Morph(reconstruction)
    name = os.path.splitext(os.path.basename(reconstruction))[0]
    types = args.type if args.type else SWC.TYPES
    morphometry = dict()

    segdata = get_segdata(morph, types)
    for point_type in set(types).difference((SWC.SOMA,)):
        pdata = segdata[segdata[:, SWC.T] == point_type]
        if pdata.size != 0:
            mdata = dict()
            mdata['degree'] = np.max(pdata[:, DEGREE]).astype(int)
            mdata['order'] = np.max(pdata[:, ORDER]).astype(int)
            mdata['breadth'] = np.max(pdata[:, BREADTH]).astype(int)
            mdata['nbranch'] = np.sum(pdata[:, BRANCH]).astype(int)
            mdata['nterm'] = np.sum(pdata[:, TERM]).astype(int)
            mdata['nstem'] = np.sum(pdata[pdata[:, SWC.P]==1][:, SWC.P]).astype(int)
            mdata['length'] = np.sum(pdata[pdata[:, SWC.P]==1][:, TOTLEN] + pdata[pdata[:, SWC.P]==1][:, LENGTH])
            mdata['area'] = np.sum(pdata[pdata[:, SWC.P]==1][:, TOTAREA] + pdata[pdata[:, SWC.P]==1][:, AREA])
            mdata['volume'] = np.sum(pdata[pdata[:, SWC.P]==1][:, TOTVOL] + pdata[pdata[:, SWC.P]==1][:, VOLUME])
            mdata['diam'] = np.mean(pdata[:, SWC.R]) * 2
            mdata['xdim'] = np.max(pdata[:, SWC.X]) - np.min(pdata[:, SWC.X])
            mdata['ydim'] = np.max(pdata[:, SWC.Y]) - np.min(pdata[:, SWC.Y])
            mdata['zdim'] = np.max(pdata[:, SWC.Z]) - np.min(pdata[:, SWC.Z])
            if not ptmap[point_type] in morphometry:
                morphometry[ptmap[point_type]] = dict()
            morphometry[ptmap[point_type]].update(mdata)
    if args.opt and 'seg' in args.opt:
        if not 'soma' in morphometry:
            morphometry['soma'] = dict()
        morphometry['soma']['_seg'] = segdata

    secmode = True if args.opt and 'sec' in args.opt else False
    secdata = get_secdata(morph, types, full_mode=secmode)
    for point_type in set(types).difference((SWC.SOMA,)):
        sdata = np.array(secdata[ptmap[point_type]])
        if sdata.size != 0:
            mdata = dict()
            mdata['seclen'] = np.mean(sdata[:, SECLEN])
            mdata['contrac'] = np.mean(sdata[:, CONTRAC])
            morphometry[ptmap[point_type]].update(mdata)
            if args.opt and 'sec' in args.opt:
                morphometry[ptmap[point_type]]['_sec'] = secdata

    return {name: morphometry}


def meter(args):
    """Computes morphometric features of the reconstruction."""
    # pylint: disable=invalid-name
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=cell-var-from-loop
    # pylint: disable=undefined-loop-variable
    ptmap = dict(zip(SWC.TYPES, ['soma', 'axon', 'dend', 'apic']))
    metric = dict()
    reconstructions = args.file
    items = zip(reconstructions, (args,) * len(reconstructions))
    with mp.Pool() as pool:
        for morphometry in pool.starmap(get_morphometry, items):
            metric.update(morphometry)

    if not args.out:
        for name in metric:
            print(name)
            for point_type in sorted(metric[name]):
                for feature in sorted(metric[name][point_type]):
                    if feature != 'sholl' and feature != '_sec' and feature != '_seg':
                        print(f'{point_type} {feature:10s} '
                              f'{metric[name][point_type][feature]:>8g}')
                    elif feature == 'sholl':
                        print(f'{point_type} {feature:10s} '
                              f'{sum(metric[name][point_type][feature]["crossings"]):>8g}')
            print()
    else:
        with open(args.out, 'w') as f:
            json.dump(metric, f, indent=4, sort_keys=True, cls=TreemEncoder)
