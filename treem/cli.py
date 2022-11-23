"""Command-line interface to package treem."""

# pylint: disable=too-many-statements

import argparse
import sys

from treem.io import SWC

from treem.commands.check import check
from treem.commands.view import view
from treem.commands.find import find
from treem.commands.modify import modify
from treem.commands.repair import repair
from treem.commands.measure import measure
from treem.commands.convert import convert

try:
    import OpenGL
    from treem.commands.render import render, _HELP
except ImportError:
    pass


def cli():
    """Command-line interface definition."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    cmd_check = subparsers.add_parser(
        'check',
        epilog='prints out error codes and IDs of error nodes; '
               'returns the number of errors',
        help='test morphology reconstruction for structural consistency')  # noqa
    cmd_check.add_argument('file', type=str,
                           help='input morphology file (swc)')
    cmd_check.add_argument('-q', dest='quiet', action='store_true',
                           help='disable output')
    cmd_check.add_argument('-o', dest='out', metavar='<str>', type=str,
                           help='save output to file (json)')
    cmd_check.set_defaults(func=check)

    cmd_view = subparsers.add_parser('view', help='view morphology')
    cmd_view.add_argument('file', type=str, nargs='+',
                          help='input morphology file (swc)')
    cmd_view.add_argument('-p', dest='type', metavar='<int>', type=int,
                          nargs='+', choices=SWC.TYPES,
                          help='point type {1,2,3,4} [all]')
    cmd_view.add_argument('-b', dest='branch', type=int, metavar='<int>',
                          nargs='+', action='append', help='branch start id')
    cmd_view.add_argument('-s', dest='sec', type=int, metavar='<int>',
                          nargs='+', action='append', help='section start id')
    cmd_view.add_argument('-m', dest='mark', metavar='<int>', type=int,
                          nargs='+', action='append', help='marker point id')
    cmd_view.add_argument('--show-id', dest='show_id', action='store_true',
                          help='show id labels')
    cmd_view.add_argument('-t', dest='title', metavar='<str>', type=str,
                          help='set figure title')
    cmd_view.add_argument('--no-axes', dest='no_axes', action='store_true',
                          help='disable axes')
    cmd_view.add_argument('--scale', dest='scale', metavar='<float>',
                          type=float, help='show scale bars, um')
    cmd_view.add_argument('-c', dest='mode', metavar='<str>', type=str,
                          choices=['neurites', 'cells', 'shadow'],
                          default='neurites',
                          help='color mode {neurites,cells,shadow} '
                               '[neurites]')
    cmd_view.add_argument('--shadow-color', dest='shadow_color',
                          metavar='<str>', type=str, default='lightgray',
                          help='shadow color [lightgray]')
    cmd_view.add_argument('--shadow-width', dest='shadow_width',
                          metavar='<float>', type=float, default=3.0,
                          help='shadow width [3.0]')
    cmd_view.add_argument('--line-width', dest='linewidth',
                          metavar='<float>', type=float, default=1.0,
                          help='line width [1.0]')
    cmd_view.add_argument('--set-color', dest='cycler_color', nargs='+',
                          metavar='<str>', type=str, 
                          help='set color (number:colorname)')
    cmd_view.add_argument('-a', dest='angle', metavar='<float>', type=float,
                          nargs=2, help='initial rotation angles, deg. '
                                        '(elevation, azimuth)')
    cmd_view.add_argument('-d', dest='dist', metavar='<float>', type=float,
                          default=10.0,
                          help='initial distance to object, rel. [10.0]')
    cmd_view.add_argument('-x', dest='xlim', metavar='<float>', type=float, default=[],
                          nargs=2, help='set limits for x-axis (min, max) [auto]')
    cmd_view.add_argument('-y', dest='ylim', metavar='<float>', type=float, default=[],
                          nargs=2, help='set limits for y-axis (min, max) [auto]')
    cmd_view.add_argument('-z', dest='zlim', metavar='<float>', type=float, default=[],
                          nargs=2, help='set limits for z-axis (min, max) [auto]')
    cmd_view.add_argument('--font', dest='font', metavar='<int>', type=int,
                          default=8, help='font size [8]')
    cmd_view.add_argument('--title-font', dest='title_font', metavar='<int>', type=int,
                          default=14, help='title font size [14]')
    cmd_view.add_argument('-g', dest='dgram', action='store_true',
                          help='show as dendrogram graph')
    cmd_view.add_argument('--dgram-ystep', dest='dgram_ystep', metavar='<float>', type=float, default=1.0,
                          help='change breadth step size in y-axis [1.0]')
    cmd_view.add_argument('--dgram-zstep', dest='dgram_zstep', metavar='<float>', type=float, default=1.0,
                          help='change breadth step size in z-axis [1.0]')
    cmd_view.add_argument('-j', dest='proj', metavar='<str>', type=str,
                          choices=['xy', 'xz', 'yz'],
                          help='projection {xy,xz,yz}')
    cmd_view.add_argument('-o', dest='out', metavar='<str>', type=str,
                          help='save image to file')
    cmd_view.set_defaults(func=view)

    cmd_find = subparsers.add_parser('find', epilog='prints out point ids',
                                     help='locate single points')
    cmd_find.add_argument('file', type=str,
                          help='input morphology file (swc)')
    cmd_find.add_argument('-p', dest='type', metavar='<int>', type=int,
                          nargs='+', choices=SWC.TYPES,
                          help='point type {1,2,3,4} [any]')
    cmd_find.add_argument('-e', dest='order', metavar='<int>', type=int,
                          nargs='+', help='branch order')
    cmd_find.add_argument('-b', dest='breadth', metavar='<int>', type=int,
                          nargs='+', help='branch breadth')
    cmd_find.add_argument('-g', dest='degree', metavar='<int>', type=int,
                          nargs='+', help='node degree')
    cmd_find.add_argument('-d', dest='diam', metavar='<float>', type=float,
                          help='diameter threshold, um')
    cmd_find.add_argument('-l', dest='length', metavar='<float>', type=float,
                          help='segment length threshold, um')
    cmd_find.add_argument('-i', dest='dist', metavar='<float>', type=float,
                          help='distance to origin threshold, um')
    cmd_find.add_argument('-s', dest='slice', metavar='<float>', type=float,
                          help='virtual slice threshold (z axis), um')
    cmd_find.add_argument('-z', dest='jump', metavar='<float>', type=float,
                          help='z-jump threshold, um')
    cmd_find.add_argument('--comp', dest='compare', metavar='<str>',
                          type=str,
                          choices=['gt', 'lt', 'eq'], default='gt',
                          help='comparison condition for threshold '
                               '{lt,eq,gt} [gt]')
    cmd_find.add_argument('-c', dest='cut', metavar='<float>', type=float,
                          help='cut plane thickness, um (z axis)')
    cmd_find.add_argument('--bottom-up', dest='bottom_up',
                          action='store_true',
                          help='slice surface down (z axis)')
    cmd_find.add_argument('--cut-find', dest='cut_find',
                          action='store_true', help='find cut plane')
    cmd_find.add_argument('--cut-find-iter', dest='cut_iter', metavar='<int>', type=int,
                          default=800, help='number of iterations [800]')
    cmd_find.add_argument('-n', dest='nodes', metavar='<int>', type=int,
                          nargs='+', help='branch nodes')
    cmd_find.add_argument('--sec', dest='sec', action='store_true',
                          help='section start ids only')
    cmd_find.add_argument('--stem', dest='stem', action='store_true',
                          help='stem ids only')
    cmd_find.set_defaults(func=find)

    cmd_modify = subparsers.add_parser('modify', help='modify morphology')
    cmd_modify.add_argument('file', type=str,
                            help='input morphology file (swc)')
    cmd_modify.add_argument('-p', dest='type', metavar='<int>', type=int,
                            nargs='+',
                            choices=set(SWC.TYPES).difference((SWC.SOMA,)),
                            help='point type {2,3,4} [all]')
    cmd_modify.add_argument('-e', dest='order', metavar='<int>', type=int,
                            nargs='+', help='branch order')
    cmd_modify.add_argument('-b', dest='breadth', metavar='<int>', type=int,
                            nargs='+', help='branch breadth')
    cmd_modify.add_argument('-i', dest='ids', metavar='<int>', type=int,
                            nargs='+', help='input ids')
    cmd_modify.add_argument('-s', dest='scale', metavar='<float>', type=float,
                            nargs=3, help='scaling factors, positive (x,y,z axes)')
    cmd_modify.add_argument('-r', dest='scale_radius', metavar='<float>',
                            type=float, help='radius scaling factor, positive')
    cmd_modify.add_argument('-t', dest='stretch', metavar='<float>',
                            type=float, help='stretching strength, rel.')
    cmd_modify.add_argument('-m', dest='smooth', metavar='<int>', type=int,
                            help='smoothing strength, iter.')
    cmd_modify.add_argument('-j', dest='jitter', metavar='<float>', type=float,
                            help='random coordinate jitter, um (max)')
    cmd_modify.add_argument('--sec', dest='sec', action='store_true',
                            help='apply jitter per section')
    cmd_modify.add_argument('-w', dest='twist', metavar='<float>', type=float,
                            help='random branch twisting, deg. (max)')
    cmd_modify.add_argument('-u', dest='prune', action='store_true',
                            help='prune branches')
    cmd_modify.add_argument('-a', dest='swap', action='store_true',
                            help='swap branches')
    cmd_modify.add_argument('--seed', dest='seed', metavar='<int>', type=int,
                            help='random seed')
    cmd_modify.add_argument('-o', dest='out', metavar='<str>', type=str,
                            default='mod.swc',
                            help='output morphology file (swc) [mod.swc]')
    cmd_modify.set_defaults(func=modify)

    cmd_repair = subparsers.add_parser('repair', help='repair morphology')
    cmd_repair.add_argument('file', type=str,
                            help='input morphology file (swc)')
    cmd_repair.add_argument('-n', dest='center', action='store_true',
                            help='center root')
    cmd_repair.add_argument('-t', dest='translate', metavar='<float>',
                            type=float, nargs=3,
                            help='translate morphology, um (x,y,z)')
    cmd_repair.add_argument('-a', dest='rotate', metavar='<float>', type=float,
                            nargs=3, help='rotate morphology, deg. '
                                          '(x,y,z axes)')
    cmd_repair.add_argument('-k', dest='shrink', metavar='<float>', type=float,
                            help='shrinkage correction factor (z axis)')
    cmd_repair.add_argument('-kxy', dest='shrink_xy', metavar='<float>',
                            type=float,
                            help='shrinkage correction factor (x,y plane)')
    cmd_repair.add_argument('--bottom-up', dest='bottom_up',
                            action='store_true',
                            help='slice surface down (z axis)')
    cmd_repair.add_argument('--seed', dest='seed', metavar='<int>', type=int,
                            help='random seed')
    cmd_repair.add_argument('-c', dest='cut', metavar='<int>', type=int,
                            nargs='+', help='cut points ids (not compatible with -l)')
    cmd_repair.add_argument('--force-repair', dest='force_repair',
                            action='store_true',
                            help='repair cuts using branches of any order')
    cmd_repair.add_argument('--graft-point-type', dest='graft_point_type', type=int,
                            choices=set(SWC.TYPES).difference((SWC.SOMA,)), default=SWC.DEND,
                            help='point type of a branch to graft on to a soma node {2,3,4} [3]')
    cmd_repair.add_argument('--del-branch', dest='del_branch',
                            action='store_true',
                            help='delete cut branches before repair')
    cmd_repair.add_argument('--keep-radii', dest='keep_radii',
                            action='store_true',
                            help='do not scale radii of repaired branches')
    cmd_repair.add_argument('-d', dest='diam', metavar='<int>', type=int,
                            nargs='+',
                            help='set diameter in points ids')
    cmd_repair.add_argument('--diam', dest='diam_mode', metavar='<str>',
                            type=str, default='joint',
                            choices=['joint', 'sec', 'order', 'breadth', 'value'],
                            help='correction mode '
                                 '{joint,sec,order,breadth,value} [joint]')
    cmd_repair.add_argument('--diam-value', dest='diam_value', metavar='<float>',
                            type=float, default=1.0,
                            help='diameter value, um [1.0]')
    cmd_repair.add_argument('--pool', dest='pool', metavar='<str>', type=str,
                            nargs='+', help='reference reconstructions for repair')
    cmd_repair.add_argument('-l', dest='delete', metavar='<int>', type=int,
                            nargs='+',
                            help='delete nodes in points ids (not compatible with -c)')
    cmd_repair.add_argument('-z', dest='zjump', metavar='<int>', type=int,
                            nargs='+', help='z-jump points ids')
    cmd_repair.add_argument('--zjump', dest='zjump_mode', metavar='<str>',
                            type=str, default='align',
                            choices=['align', 'split', 'tilt', 'join'],
                            help='correction mode '
                                 '{align,split,tilt,join} [align]')
    cmd_repair.add_argument('-r', dest='res', metavar='<float>', type=float,
                            help='sampling resolution, um')
    cmd_repair.add_argument('-o', dest='out', metavar='<str>', type=str,
                            default='rep.swc',
                            help='output morphology file (swc) [rep.swc]')
    cmd_repair.add_argument('-v', dest='verbose', action='store_true',
                            help='verbose output')
    cmd_repair.set_defaults(func=repair)

    cmd_measure = subparsers.add_parser('measure', help='measure morphology')
    cmd_measure.add_argument('file', type=str, nargs='+',
                             help='input morphology file (swc)')
    cmd_measure.add_argument('-p', dest='type', metavar='<int>', type=int,
                             nargs='+', choices=SWC.TYPES,
                             help='point type {1,2,3,4} [all]')
    cmd_measure.add_argument('-a', dest='opt', metavar='<str>', type=str,
                             nargs='+', choices=['dist', 'path', 'sec', 'sholl'],
                             help='optional feature {dist,path,sholl}')
    cmd_measure.add_argument('--sholl-res', dest='sholl_res', metavar='<float>',
                             type=float, default=10.0,
                             help='sholl sampling resolution, um [10.0]')
    cmd_measure.add_argument('--sholl-proj', dest='sholl_proj', metavar='<str>',
                             type=str, choices=['xy', 'xz', 'yz'],
                             help='sholl projection {xy,xz,yz} [3d]')
    cmd_measure.add_argument('-o', dest='out', metavar='<str>', type=str,
                             help='output morphometric file (json)')
    cmd_measure.set_defaults(func=measure)

    cmd_convert = subparsers.add_parser('convert', help='convert input file')
    cmd_convert.add_argument('file', type=str,
                             help='input morphology file (swc)')
    cmd_convert.add_argument('-p', dest='type', metavar='<int>', type=int,
                             nargs='+', choices=SWC.TYPES,
                             help='point type {1,2,3,4} [all]')
    cmd_convert.add_argument('-o', dest='out', metavar='<str>', type=str,
                             default='inp.swc',
                             help='converted morphology file (swc) [inp.swc]')
    cmd_convert.add_argument('-q', dest='quiet', action='store_true',
                             help='disable output')
    cmd_convert.set_defaults(func=convert)

    if 'OpenGL' in sys.modules:
        cmd_render = subparsers.add_parser(
            'render', help='show 3D model', epilog=_HELP,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        cmd_render.add_argument('file', type=str,
                                help='input morphology file (swc)')
        cmd_render.set_defaults(func=render)

    args = parser.parse_args()
    sys.exit(args.func(args))
