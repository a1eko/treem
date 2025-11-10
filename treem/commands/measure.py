"""Implementation of CLI measure command."""

import os
import json
import math

import multiprocessing as mp
import numpy as np

from treem import Morph, SWC

from treem.io import TreemEncoder
from treem.utils.geom import norm
from treem.morph import get_segdata, SEG


def _measure_neurites(morph, morphometry, name, types, ptmap, opt=[]):
    """Computes morphometry of non-soma nodes."""
    center = morph.root.coord()
    if 'seg' in opt:
        segdata = get_segdata(morph)
    for point_type in set(types).difference((SWC.SOMA,)):
        mdata = []
        for sec in filter(lambda x: x[0].type() == point_type,
                          morph.root.sections()):
            head = sec[0]
            tail = sec[-1]
            seclen = morph.length(sec)
            chord = norm(tail.coord() - head.parent.coord())
            coords = morph.coords(sec)
            xmin, ymin, zmin = np.min(coords, axis=0)
            xmax, ymax, zmax = np.max(coords, axis=0)
            dist = np.max(np.linalg.norm(coords - center, axis=1))
            mdata.append(
                [tail.degree(), head.order(), tail.breadth(),
                 seclen, chord / seclen,
                 morph.area(sec), morph.volume(sec),
                 morph.radii(sec).mean() * 2,
                 xmin, xmax, ymin, ymax, zmin, zmax,
                 dist])
        if mdata:
            ndata = np.array(mdata)
            d = morphometry[name][ptmap[point_type]] = {}
            d['degree'] = np.max(ndata[:, 0], axis=0).astype(int)
            d['order'] = np.max(ndata[:, 1], axis=0).astype(int)
            d['breadth'] = np.max(ndata[:, 2], axis=0).astype(int)
            d['nbranch'] = sum(1 for x in ndata[:, 0] if x > 1)
            d['nterm'] = sum(1 for x in ndata[:, 0] if x == 0)
            d['nstem'] = sum(1 for x in ndata[:, 1] if x == 1)
            d['length'] = np.sum(ndata[:, 3], axis=0)
            d['seclen'] = np.mean(ndata[:, 3], axis=0)
            d['contrac'] = np.mean(ndata[:, 4], axis=0)
            d['area'] = np.sum(ndata[:, 5], axis=0)
            d['volume'] = np.sum(ndata[:, 6], axis=0)
            d['diam'] = np.mean(ndata[:, 7], axis=0)
            d['xdim'] = (np.max(ndata[:, 9], axis=0) - np.min(ndata[:, 8], axis=0))
            d['ydim'] = (np.max(ndata[:, 11], axis=0) - np.min(ndata[:, 10], axis=0))
            d['zdim'] = (np.max(ndata[:, 13], axis=0) - np.min(ndata[:, 12], axis=0))
            d['dist'] = np.max(ndata[:, 14], axis=0)
            if 'sec' in opt:
                d['_sec'] = ndata.transpose()
            if 'seg' in opt:
                sel = np.nonzero(segdata[:, SEG.T] == point_type)
                d['_seg'] = segdata[sel]


def _measure_soma(morph, morphometry, name, types, ptmap):
    """Computes morphometry of soma nodes."""
    for point_type in set(types).intersection((SWC.SOMA,)):
        mdata = []
        for sec in filter(lambda x: x[0].type() == point_type,
                          morph.root.sections()):
            if len(sec) > 1:
                area = morph.area(sec)
                volume = morph.volume(sec)
            else:
                area = 4 * math.pi * sec[0].radius()**2
                volume = 4 / 3 * math.pi * sec[0].radius()**3
            mdata.append([area, volume, morph.radii(sec).mean() * 2])
        if mdata:
            ndata = np.array(mdata)
            d = morphometry[name][ptmap[point_type]] = {}
            d['area'] = np.sum(ndata[:, 0], axis=0)
            d['volume'] = np.sum(ndata[:, 1], axis=0)
            d['diam'] = np.mean(ndata[:, 2], axis=0)
            d['xroot'], d['yroot'], d['zroot'] = morph.root.coord()


def _measure_path(morph, morphometry, name, types, ptmap):
    """Computes path distance for non-soma nodes."""
    path = {}
    for node in morph.root.leaves():
        point_type = node.type()
        if point_type in set(types).difference((SWC.SOMA,)):
            if point_type not in path:
                path[point_type] = []
            path_length = sum(x.length() for x in node.walk(reverse=True))
            path[point_type].append(path_length)
    for point_type in path:
        d = morphometry[name][ptmap[point_type]]
        d['path'] = max(path[point_type])


def _get_sholl_center(morph, sholl_proj):
    """Finds center of reconstruction for given projection."""
    if sholl_proj == 'xy':
        center = morph.root.v[SWC.XY]
    elif sholl_proj == 'xz':
        center = morph.root.v[SWC.XZ]
    elif sholl_proj == 'yz':
        center = morph.root.v[SWC.YZ]
    else:
        center = morph.root.coord()
    return center


def _get_sholl_segment(node, sholl_proj):
    """Locates Sholl segment."""
    if sholl_proj == 'xy':
        c1 = node.parent.v[SWC.XY]
        c2 = node.v[SWC.XY]
    elif sholl_proj == 'xz':
        c1 = node.parent.v[SWC.XZ]
        c2 = node.v[SWC.XZ]
    elif sholl_proj == 'yz':
        c1 = node.parent.v[SWC.YZ]
        c2 = node.v[SWC.YZ]
    else:
        c1 = node.parent.coord()
        c2 = node.coord()
    return c1, c2


def _collect_sholl_data(morph, types, sholl_res, sholl_proj):
    """Collects data needed to calcuate Sholl intersections."""
    c0 = _get_sholl_center(morph, sholl_proj)
    selected_types = set(types).difference((SWC.SOMA,))
    sholl_data = {}
    for node in morph.root.walk():
        point_type = node.type()
        if point_type in set(types).difference((SWC.SOMA,)):
            if point_type not in sholl_data:
                sholl_data[point_type] = {}
            c1, c2 = _get_sholl_segment(node, sholl_proj)
            n1 = math.ceil(np.linalg.norm(c1 - c0) / sholl_res)
            n2 = math.ceil(np.linalg.norm(c2 - c0) / sholl_res)
            for circle in range(n1, n2):
                if circle not in sholl_data[point_type]:
                    sholl_data[point_type][circle] = 0
                sholl_data[point_type][circle] += 1
    return sholl_data


def _measure_sholl(morph, morphometry, name, types, ptmap, sholl_res, sholl_proj):
    """Computes Sholl intersections."""
    sholl_data = _collect_sholl_data(morph, types, sholl_res, sholl_proj)
    for point_type in sholl_data:
        radii = [x * sholl_res for x in sholl_data[point_type]]
        cross = [sholl_data[point_type][x] for x in sholl_data[point_type]]
        d = morphometry[name][ptmap[point_type]]
        d['sholl'] = {'radii': radii, 'crossings': cross}


def get_morphometry(reconstruction, args):
    """Computes morphometric features of a reconstruction."""
    types = args.type if args.type else SWC.TYPES
    ptmap = dict(zip(SWC.TYPES, ['soma', 'axon', 'dend', 'apic']))
    morphometry = {}

    morph = Morph(reconstruction)
    name = os.path.splitext(os.path.basename(reconstruction))[0]
    morphometry[name] = {}

    opt = args.opt if args.opt else []
    _measure_neurites(morph, morphometry, name, types, ptmap, opt=opt)
    _measure_soma(morph, morphometry, name, types, ptmap)

    if 'path' in opt:
        _measure_path(morph, morphometry, name, types, ptmap)
    if 'sholl' in opt:
        _measure_sholl(morph, morphometry, name, types, ptmap, sholl_res=args.sholl_res, sholl_proj=args.sholl_proj)

    return morphometry


def measure(args):
    """Computes morphometric features of multiple reconstructions."""
    metric = {}
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
                    if feature not in ('sholl', '_sec', '_seg'):
                        print(f'{point_type} {feature:10s} '
                              f'{metric[name][point_type][feature]:>8g}')
                    elif feature == 'sholl':
                        print(f'{point_type} {feature:10s} '
                              f'{sum(metric[name][point_type][feature]["crossings"]):>8g}')
            print()
    else:
        with open(args.out, 'w', encoding='utf-8') as file:
            json.dump(metric, file, indent=4, sort_keys=True, cls=TreemEncoder)
