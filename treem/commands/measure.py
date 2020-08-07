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

    if not args.out:
        for name in metric:
            print(name)
            for point_type in sorted(metric[name]):
                for feature in sorted(metric[name][point_type]):
                    print(f'{point_type} {feature:10s} '
                          f'{metric[name][point_type][feature]:>8g}')
            print()
    else:
        with open(args.out, 'w') as f:
            json.dump(metric, f, indent=4, sort_keys=True, cls=TreemEncoder)
