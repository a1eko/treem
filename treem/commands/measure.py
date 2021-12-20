"""Implementation of CLI measure command."""

import os
import json
import math

import numpy as np

from treem import Morph, SWC

from treem.io import TreemEncoder
from treem.utils.geom import norm


def measure(args):
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
                    dist[point_type].append(np.linalg.norm(node.coord() - c0))
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
            c0 = morph.root.coord()
            sholl_data = dict()
            for node in morph.root.walk():
                point_type = node.type()
                if point_type in set(types).difference((SWC.SOMA,)):
                    if point_type not in sholl_data:
                        sholl_data[point_type] = dict()
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
                    if feature != 'sholl':
                        print(f'{point_type} {feature:10s} '
                              f'{metric[name][point_type][feature]:>8g}')
                    else:
                        print(f'{point_type} {feature:10s} ')
                        radii = metric[name][point_type][feature]['radii']
                        cross = metric[name][point_type][feature]['crossings']
                        for x, y in zip(radii,cross):
                            print(11*' ', f'{x:>8g}, {y}')
            print()
    else:
        with open(args.out, 'w') as f:
            json.dump(metric, f, indent=4, sort_keys=True, cls=TreemEncoder)
