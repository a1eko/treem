"""Implementation of CLI measure command."""

import os
import json
import math

import numpy as np
import multiprocessing as mp

from treem import Morph, SWC

from treem.io import TreemEncoder
from treem.utils.geom import norm


def measure0(args):
    """Computes morphometric features of the reconstruction."""
    # pylint: disable=invalid-name
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=cell-var-from-loop
    # pylint: disable=undefined-loop-variable
    types = args.type if args.type else SWC.TYPES
    ptmap = dict(zip(SWC.TYPES, ['soma', 'axon', 'dend', 'apic']))
    metric = dict()
    for reconstruction in args.file:
        morph = Morph(reconstruction)
        name = os.path.splitext(os.path.basename(reconstruction))[0]
        metric[name] = dict()

        for point_type in set(types).difference((SWC.SOMA,)):
            mdata = list()
            for sec in filter(lambda x: x[0].type() == point_type,
                              morph.root.sections()):
                head = sec[0]
                tail = sec[-1]
                seclen = morph.length(sec)
                chord = norm(tail.coord() - head.parent.coord())
                coords = morph.coords(sec)
                xmin, ymin, zmin = np.min(coords, axis=0)
                xmax, ymax, zmax = np.max(coords, axis=0)
                mdata.append(
                    [tail.degree(), head.order(), tail.breadth(),
                     seclen, chord / seclen,
                     morph.area(sec), morph.volume(sec),
                     morph.radii(sec).mean()*2,
                     xmin, xmax, ymin, ymax, zmin, zmax])
            if mdata:
                ndata = np.array(mdata)
                d = metric[name][ptmap[point_type]] = dict()
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
                d['xdim'] = (np.max(ndata[:, 9], axis=0)
                             - np.min(ndata[:, 8], axis=0))
                d['ydim'] = (np.max(ndata[:, 11], axis=0)
                             - np.min(ndata[:, 10], axis=0))
                d['zdim'] = (np.max(ndata[:, 13], axis=0)
                             - np.min(ndata[:, 12], axis=0))
                if args.opt and 'sec' in args.opt:
                    d['_sec'] = ndata.transpose()

        for point_type in set(types).intersection((SWC.SOMA,)):
            mdata = list()
            for sec in filter(lambda x: x[0].type() == point_type,
                              morph.root.sections()):
                if len(sec) > 1:
                    area = morph.area(sec)
                    volume = morph.volume(sec)
                else:
                    area = 4*math.pi*sec[0].radius()**2
                    volume = 4/3*math.pi*sec[0].radius()**3
                mdata.append([area, volume, morph.radii(sec).mean()*2])
            if mdata:
                ndata = np.array(mdata)
                d = metric[name][ptmap[point_type]] = dict()
                d['area'] = np.sum(ndata[:, 0], axis=0)
                d['volume'] = np.sum(ndata[:, 1], axis=0)
                d['diam'] = np.mean(ndata[:, 2], axis=0)
                d['xroot'], d['yroot'], d['zroot'] = morph.root.coord()

        if args.opt and 'dist' in args.opt:
            dist = dict()
            c0 = morph.root.coord()
            for node in morph.root.walk():
                point_type = node.type()
                if point_type in set(types).difference((SWC.SOMA,)):
                    if point_type not in dist:
                        dist[point_type] = list()
                    dist[point_type].append(node.dist(c0))
            for point_type in dist:
                d = metric[name][ptmap[point_type]]
                d['dist'] = max(dist[point_type])

        if args.opt and 'path' in args.opt:
            path = dict()
            for node in morph.root.leaves():
                point_type = node.type()
                if point_type in set(types).difference((SWC.SOMA,)):
                    if point_type not in path:
                        path[point_type] = list()
                    path_length = sum([x.length() for x in node.walk(reverse=True)])
                    path[point_type].append(path_length)
            for point_type in path:
                d = metric[name][ptmap[point_type]]
                d['path'] = max(path[point_type])

        if args.opt and 'sholl' in args.opt:
            if args.sholl_proj and args.sholl_proj == 'xy':
                c0 = morph.root.v[SWC.XY]
            elif args.sholl_proj and args.sholl_proj == 'xz':
                c0 = morph.root.v[SWC.XZ]
            elif args.sholl_proj and args.sholl_proj == 'yz':
                c0 = morph.root.v[SWC.YZ]
            else:
                c0 = morph.root.coord()
            sholl_data = dict()
            for node in morph.root.walk():
                point_type = node.type()
                if point_type in set(types).difference((SWC.SOMA,)):
                    if point_type not in sholl_data:
                        sholl_data[point_type] = dict()
                    if args.sholl_proj and args.sholl_proj == 'xy':
                        c1 = node.parent.v[SWC.XY]
                        c2 = node.v[SWC.XY]
                    elif args.sholl_proj and args.sholl_proj == 'xz':
                        c1 = node.parent.v[SWC.XZ]
                        c2 = node.v[SWC.XZ]
                    elif args.sholl_proj and args.sholl_proj == 'yz':
                        c1 = node.parent.v[SWC.YZ]
                        c2 = node.v[SWC.YZ]
                    else:
                        c1 = node.parent.coord()
                        c2 = node.coord()
                    n1 = math.ceil(np.linalg.norm(c1 - c0) / args.sholl_res)
                    n2 = math.ceil(np.linalg.norm(c2 - c0) / args.sholl_res)
                    for circle in range(n1, n2):
                        if circle not in sholl_data[point_type]:
                            sholl_data[point_type][circle] = 0
                        sholl_data[point_type][circle] += 1
            for point_type in sholl_data:
                radii = [x * args.sholl_res for x in sholl_data[point_type]]
                cross = [sholl_data[point_type][x] for x in sholl_data[point_type]]
                d = metric[name][ptmap[point_type]]
                d['sholl'] = {'radii': radii, 'crossings': cross}

    if not args.out:
        for name in metric:
            print(name)
            for point_type in sorted(metric[name]):
                for feature in sorted(metric[name][point_type]):
                    if feature != 'sholl' and feature != '_sec':
                        print(f'{point_type} {feature:10s} '
                              f'{metric[name][point_type][feature]:>8g}')
                    elif feature == 'sholl':
                        print(f'{point_type} {feature:10s} '
                              f'{sum(metric[name][point_type][feature]["crossings"]):>8g}')
                        #radii = metric[name][point_type][feature]['radii']
                        #cross = metric[name][point_type][feature]['crossings']
                        #for x, y in zip(radii,cross):
                        #    print(11*' ', f'{x:>8g}, {y}')
            print()
    else:
        with open(args.out, 'w') as f:
            json.dump(metric, f, indent=4, sort_keys=True, cls=TreemEncoder)


def get_morphometry(reconstruction, args):
    """Computes morphometric features of a reconstruction."""
    # pylint: disable=invalid-name
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=cell-var-from-loop
    # pylint: disable=undefined-loop-variable
    types = args.type if args.type else SWC.TYPES
    ptmap = dict(zip(SWC.TYPES, ['soma', 'axon', 'dend', 'apic']))
    morphometry = dict()

    morph = Morph(reconstruction)
    name = os.path.splitext(os.path.basename(reconstruction))[0]
    morphometry[name] = dict()
    c0 = morph.root.coord()

    for point_type in set(types).difference((SWC.SOMA,)):
        mdata = list()
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
            mdata.append(
                [tail.degree(), head.order(), tail.breadth(),
                 seclen, chord / seclen,
                 morph.area(sec), morph.volume(sec),
                 morph.radii(sec).mean()*2,
                 xmin, xmax, ymin, ymax, zmin, zmax,
                 dist])
        if mdata:
            ndata = np.array(mdata)
            d = morphometry[name][ptmap[point_type]] = dict()
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
            d['xdim'] = (np.max(ndata[:, 9], axis=0)
                         - np.min(ndata[:, 8], axis=0))
            d['ydim'] = (np.max(ndata[:, 11], axis=0)
                         - np.min(ndata[:, 10], axis=0))
            d['zdim'] = (np.max(ndata[:, 13], axis=0)
                         - np.min(ndata[:, 12], axis=0))
            d['dist'] = np.max(ndata[:, 14], axis=0)
            print(f'{np.max(ndata[:, 14], axis=0)=}')
            if args.opt and 'sec' in args.opt:
                d['_sec'] = ndata.transpose()

    for point_type in set(types).intersection((SWC.SOMA,)):
        mdata = list()
        for sec in filter(lambda x: x[0].type() == point_type,
                          morph.root.sections()):
            if len(sec) > 1:
                area = morph.area(sec)
                volume = morph.volume(sec)
            else:
                area = 4*math.pi*sec[0].radius()**2
                volume = 4/3*math.pi*sec[0].radius()**3
            mdata.append([area, volume, morph.radii(sec).mean()*2])
        if mdata:
            ndata = np.array(mdata)
            d = morphometry[name][ptmap[point_type]] = dict()
            d['area'] = np.sum(ndata[:, 0], axis=0)
            d['volume'] = np.sum(ndata[:, 1], axis=0)
            d['diam'] = np.mean(ndata[:, 2], axis=0)
            d['xroot'], d['yroot'], d['zroot'] = morph.root.coord()

    if args.opt and 'path' in args.opt:
        path = dict()
        for node in morph.root.leaves():
            point_type = node.type()
            if point_type in set(types).difference((SWC.SOMA,)):
                if point_type not in path:
                    path[point_type] = list()
                path_length = sum([x.length() for x in node.walk(reverse=True)])
                path[point_type].append(path_length)
        for point_type in path:
            d = morphometry[name][ptmap[point_type]]
            d['path'] = max(path[point_type])

    if args.opt and 'sholl' in args.opt:
        if args.sholl_proj and args.sholl_proj == 'xy':
            c0 = morph.root.v[SWC.XY]
        elif args.sholl_proj and args.sholl_proj == 'xz':
            c0 = morph.root.v[SWC.XZ]
        elif args.sholl_proj and args.sholl_proj == 'yz':
            c0 = morph.root.v[SWC.YZ]
        else:
            c0 = morph.root.coord()
        sholl_data = dict()
        for node in morph.root.walk():
            point_type = node.type()
            if point_type in set(types).difference((SWC.SOMA,)):
                if point_type not in sholl_data:
                    sholl_data[point_type] = dict()
                if args.sholl_proj and args.sholl_proj == 'xy':
                    c1 = node.parent.v[SWC.XY]
                    c2 = node.v[SWC.XY]
                elif args.sholl_proj and args.sholl_proj == 'xz':
                    c1 = node.parent.v[SWC.XZ]
                    c2 = node.v[SWC.XZ]
                elif args.sholl_proj and args.sholl_proj == 'yz':
                    c1 = node.parent.v[SWC.YZ]
                    c2 = node.v[SWC.YZ]
                else:
                    c1 = node.parent.coord()
                    c2 = node.coord()
                n1 = math.ceil(np.linalg.norm(c1 - c0) / args.sholl_res)
                n2 = math.ceil(np.linalg.norm(c2 - c0) / args.sholl_res)
                for circle in range(n1, n2):
                    if circle not in sholl_data[point_type]:
                        sholl_data[point_type][circle] = 0
                    sholl_data[point_type][circle] += 1
        for point_type in sholl_data:
            radii = [x * args.sholl_res for x in sholl_data[point_type]]
            cross = [sholl_data[point_type][x] for x in sholl_data[point_type]]
            d = morphometry[name][ptmap[point_type]]
            d['sholl'] = {'radii': radii, 'crossings': cross}

    return morphometry


def measure(args):
    """Computes morphometric features of multiple reconstructions."""
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
