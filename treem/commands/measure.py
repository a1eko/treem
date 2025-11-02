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


def _prepare_non_soma_section_data(morph, types, c0):
    """Calculates morphometric data for all sections of non-soma types."""
    section_data_by_type = {}
    # 15 columns of data are collected per section
    # [degree, order, breadth, seclen, contract, area, volume, diam, xmin, xmax, ymin, ymax, zmin, zmax, dist]
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
            dist = np.max(np.linalg.norm(coords - c0, axis=1))
            mdata.append([
                tail.degree(), head.order(), tail.breadth(), seclen,
                chord / seclen, morph.area(sec), morph.volume(sec),
                morph.radii(sec).mean() * 2,
                xmin, xmax, ymin, ymax, zmin, zmax, dist
            ])
        if mdata:
            section_data_by_type[point_type] = np.array(mdata)
    return section_data_by_type


def _summarize_non_soma_metrics(d, ndata, args, point_type, segdata=None):
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
    if args.opt and 'sec' in args.opt:
        d['_sec'] = ndata.transpose()
    if args.opt and 'seg' in args.opt and segdata is not None:
        sel = np.nonzero(segdata[:, SEG.T] == point_type)
        d['_seg'] = segdata[sel]
    return d


def _calculate_soma_metrics(morph, types, ptmap, morphometry, name):
    """Calculates area, volume, and diameter for soma sections."""
    for point_type in set(types).intersection((SWC.SOMA,)):
        mdata = []
        for sec in filter(lambda x: x[0].type() == point_type,
                          morph.root.sections()):
            if len(sec) > 1:
                area = morph.area(sec)
                volume = morph.volume(sec)
            else:
                # single-point soma calculation
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


def _calculate_path_metrics(morph, types, ptmap, morphometry, name):
    """Calculates the maximum path length for each point type."""
    path = {}
    for node in morph.root.leaves():
        point_type = node.type()
        if point_type in set(types).difference((SWC.SOMA,)):
            if point_type not in path:
                path[point_type] = []
            # calculate path length by summing lengths of nodes walked in reverse
            path_length = sum(x.length() for x in node.walk(reverse=True))
            path[point_type].append(path_length)
    for point_type, lengths in path.items():
        if ptmap[point_type] in morphometry[name]:
            d = morphometry[name][ptmap[point_type]]
            d['path'] = max(lengths)


def _get_sholl_center(morph, args):
    """Determines the center coordinate for Sholl analysis based on projection."""
    if args.sholl_proj:
        proj = args.sholl_proj.lower()
        if proj == 'xy':
            return morph.root.v[SWC.XY]
        if proj == 'xz':
            return morph.root.v[SWC.XZ]
        if proj == 'yz':
            return morph.root.v[SWC.YZ]
    # default to 3D coordinate
    return morph.root.coord()


def _get_sholl_coords(node, args):
    """Determines the coordinates for Sholl segment based on projection."""
    proj = args.sholl_proj.lower() if args.sholl_proj else None
    if proj == 'xy':
        return node.parent.v[SWC.XY], node.v[SWC.XY]
    if proj == 'xz':
        return node.parent.v[SWC.XZ], node.v[SWC.XZ]
    if proj == 'yz':
        return node.parent.v[SWC.YZ], node.v[SWC.YZ]
    # default to 3D coordinates
    return node.parent.coord(), node.coord()


def _count_sholl_crossings(morph, args, types, c0):
    """Counts Sholl crossings for all relevant nodes and radii."""
    sholl_data = {}

    # iterate over all nodes to collect crossings
    for node in morph.root.walk():
        point_type = node.type()

        if point_type in set(types).difference((SWC.SOMA,)):
            if point_type not in sholl_data:
                sholl_data[point_type] = {}

            c1, c2 = _get_sholl_coords(node, args)

            # calculate radii indices
            n1 = math.ceil(np.linalg.norm(c1 - c0) / args.sholl_res)
            n2 = math.ceil(np.linalg.norm(c2 - c0) / args.sholl_res)

            # count crossings for each circle (bin)
            for circle in range(min(n1, n2), max(n1, n2) + 1):
                if circle not in sholl_data[point_type]:
                    sholl_data[point_type][circle] = 0
                sholl_data[point_type][circle] += 1

    return sholl_data


def _calculate_sholl_analysis(morph, args, types, ptmap, morphometry, name):
    """Performs Sholl analysis."""
    c0 = _get_sholl_center(morph, args)
    sholl_data = _count_sholl_crossings(morph, args, types, c0)
    # format and save Sholl data
    for point_type, data in sholl_data.items():
        radii = [r * args.sholl_res for r in data]
        cross = [data[r] for r in data]
        if ptmap[point_type] in morphometry[name]:
            d = morphometry[name][ptmap[point_type]]
            d['sholl'] = {'radii': radii, 'crossings': cross}


def _format_and_print_metrics(metric):
    """Handles the output formatting logic."""
    # This function contains the logic extracted from measure()
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


def get_morphometry(reconstruction, args):
    """Computes morphometric features of a reconstruction."""
    types = args.type if args.type else SWC.TYPES
    ptmap = dict(zip(SWC.TYPES, ['soma', 'axon', 'dend', 'apic']))
    morph = Morph(reconstruction)
    name = os.path.splitext(os.path.basename(reconstruction))[0]
    morphometry = {name: {}}
    c0 = morph.root.coord()
    segdata = get_segdata(morph) if args.opt and 'seg' in args.opt else None

    # non-soma metrics
    section_data_by_type = _prepare_non_soma_section_data(morph, types, c0)
    for point_type, ndata in section_data_by_type.items():
        d = morphometry[name][ptmap[point_type]] = {}
        _summarize_non_soma_metrics(d, ndata, args, point_type, segdata)

    # soma metrics
    _calculate_soma_metrics(morph, types, ptmap, morphometry, name)

    # path metrics
    if args.opt and 'path' in args.opt:
        _calculate_path_metrics(morph, types, ptmap, morphometry, name)

    # sholl analysis
    if args.opt and 'sholl' in args.opt:
        _calculate_sholl_analysis(morph, args, types, ptmap, morphometry, name)

    return morphometry


def measure(args):
    """Computes morphometric features of multiple reconstructions."""
    metric = {}
    reconstructions = args.file
    items = zip(reconstructions, (args,) * len(reconstructions))

    # use multiprocessing pool for parallel computation
    with mp.Pool() as pool:
        for morphometry in pool.starmap(get_morphometry, items):
            metric.update(morphometry)

    # output formatting logic is now simplified
    if not args.out:
        _format_and_print_metrics(metric)
    else:
        with open(args.out, 'w', encoding='utf-8') as file:
            json.dump(metric, file, indent=4, sort_keys=True, cls=TreemEncoder)
