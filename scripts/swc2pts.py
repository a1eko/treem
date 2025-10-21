#!/usr/bin/python3
"""
Convert SWC files to connected points.

SWC nodes are combined into section lines and saved as Python dictionary in
JSON format.
"""

import multiprocessing as mp
import numpy as np
import argparse
import json
import os

from treem import Morph, SWC
from treem.io import TreemEncoder


examples = """
Usage example code:
  pts = json.load(open('pts.json'))
  for cell in pts:
      for neurite in pts[cell]:
          for sec in pts[cell][neurite]:
              a = numpy.array(sec)
              x, y, z = a.T
              plot(x, y, z, color='black')
"""


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=examples)
    parser.add_argument('file', type=str, nargs='+', help='input file (swc)')
    parser.add_argument('-o', dest='out', type=str, default='pts.json',
                        help='output file [pts.json]')
    return parser.parse_args()


def get_lines(reconstruction):
    morph = Morph(reconstruction)
    name = os.path.splitext(os.path.basename(reconstruction))[0]
    ptmap = dict(zip(SWC.TYPES, ['soma', 'axon', 'dend', 'apic']))
    lines = {}
    lines[name] = {}
    for point_type in SWC.TYPES:
        points = list()
        for sec in filter(lambda x: x[0].type() == point_type,
                          morph.root.sections()):
            points.append(morph.coords(sec))
        for bif in filter(lambda x: x.type() == point_type,
                          morph.root.forks()):
            b = bif.coord()
            for child in bif.siblings:
                c = child.coord()
                a = np.array([b, c])
                points.append(a)
        r = morph.root.coord()
        for stem in filter(lambda x: x.type() == point_type,
                           morph.stems()):
            s = stem.coord()
            a = np.array([r, s])
            points.append(a)
        if points:
            lines[name][ptmap[point_type]] = points
    return lines


def main(args):
    pts = {}
    with mp.Pool() as pool:
        for lines in pool.map(get_lines, args.file):
            pts.update(lines)
    with open(args.out, 'w') as f:
        json.dump(pts, f, cls=TreemEncoder)


if __name__ == '__main__':
    main(parse_args())
