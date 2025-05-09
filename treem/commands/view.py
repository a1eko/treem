"""Implementation of CLI view command."""

import matplotlib.pyplot as plt
import matplotlib as mpl

from cycler import cycler

from treem.morph import Morph
from treem.morph import DGram
from treem.io import SWC

from treem.utils.plot import plot_neuron
from treem.utils.plot import plot_section
from treem.utils.plot import plot_tree
from treem.utils.plot import plot_points


_colors = ('crimson', 'dodgerblue', 'darkgrey', 'royalblue', 'limegreen',
           'orchid', 'red', 'purple', 'orange', 'darkturquoise')
_NCOLORS = len(_colors)

# mpl.rcParams['lines.linewidth'] = 1.0
# mpl.rcParams.update({'font.size': 8})
mpl.rcParams['axes.prop_cycle'] = cycler(color=_colors)


def view(args):
    """Display neuron morphology structure."""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=expression-not-assigned
    plt.rc('font', size=args.font)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')  # pylint: disable=invalid-name
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.set_proj_type('ortho')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.grid(False)

    types = args.type if args.type else SWC.TYPES
    if args.title:
        fig.suptitle(args.title, fontsize=args.title_font)
    if args.no_axes:
        ax.set_axis_off()

    if args.cycler_color:
        colors = list(_colors)
        for x in args.cycler_color:  # pylint: disable=invalid-name
            i, colorname = x.split(':')
            i = int(i)
            if 0 <= i < _NCOLORS:
                colors[i] = colorname
        mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)

    if args.mode == 'neurites':
        for count, file_name in enumerate(reversed(args.file)):
            if not args.dgram:
                morph = Morph(file_name)
            else:
                morph = DGram(source=file_name, zorder=count, ystep=args.dgram_ystep,
                              zstep=args.dgram_zstep, types=types)
            plot_neuron(ax, morph, types, linewidth=args.linewidth)
    elif args.mode == 'cells':
        for count, file_name in enumerate(reversed(args.file)):
            if not args.dgram:
                morph = Morph(file_name)
            else:
                morph = DGram(source=file_name, zorder=count, ystep=args.dgram_ystep,
                              zstep=args.dgram_zstep, types=types)
            colors = {k: f'C{count % _NCOLORS}' for k in types}
            plot_neuron(ax, morph, types, colors=colors, linewidth=args.linewidth)
    elif args.mode == 'shadow':
        for file_name in reversed(args.file[1:]):
            colors = {k: args.shadow_color for k in types}
            if not args.dgram:
                morph = Morph(file_name)
            else:
                morph = DGram(source=file_name, ystep=args.dgram_ystep,
                              zstep=args.dgram_zstep, types=types)
            plot_neuron(ax, morph, types, colors=colors,
                        linewidth=args.shadow_width)
        if not args.dgram:
            morph = Morph(args.file[0])
        else:
            morph = DGram(source=args.file[0], ystep=args.dgram_ystep,
                          zstep=args.dgram_zstep, types=types)
        plot_neuron(ax, morph, types, linewidth=args.linewidth)

    if args.branch:
        for group in args.branch:
            # pylint: disable=cell-var-from-loop
            # pylint: disable=undefined-loop-variable
            nodes = filter(lambda x: x.ident() in group, morph.root.walk())
            nodes = filter(lambda x: x.type() in types, nodes)
            for branch in nodes:
                plot_tree(ax, branch, morph.data,
                          linewidth=1.5 * args.linewidth, color='C5')
                if args.show_id:
                    plot_points(ax, morph, group, types,
                                show_id=args.show_id, markersize=6 * args.linewidth)

    if args.sec:
        for group in args.sec:
            # pylint: disable=undefined-loop-variable
            # pylint: disable=cell-var-from-loop
            nodes = filter(lambda x: x.ident() in group, morph.root.walk())
            nodes = filter(lambda x: x.type() in types, nodes)
            for sec in nodes:
                plot_section(ax, sec, morph.data,
                             linewidth=1.5 * args.linewidth, color='C5')
                if args.show_id:
                    plot_points(ax, morph, group, types,
                                show_id=args.show_id, markersize=6 * args.linewidth)

    if args.mark:
        for group in args.mark:
            plot_points(ax, morph, group, types,
                        show_id=args.show_id, markersize=6 * args.linewidth)

    if args.angle:
        ax.view_init(args.angle[0], args.angle[1])

    if args.proj:
        if args.proj.lower() == 'xy':
            ax.view_init(89.99, -90.01)
            ax.set_zlabel('')
            ax.set_zticks([])
        if args.proj.lower() == 'xz':
            ax.view_init(0.00, -90.01)
            ax.set_ylabel('')
            ax.set_yticks([])
        if args.proj.lower() == 'yz':
            ax.view_init(0.00, 0.01)
            ax.set_xlabel('')
            ax.set_xticks([])

    #if args.dist:
    #    ax.dist = args.dist

    xmin = ax.xy_dataLim.xmin
    ymin = ax.xy_dataLim.ymin
    zmin = ax.zz_dataLim.xmin
    xmax = ax.xy_dataLim.xmax
    ymax = ax.xy_dataLim.ymax
    zmax = ax.zz_dataLim.xmax
    smax = max(max(ax.xy_dataLim.size), max(ax.zz_dataLim.size))  # pylint: disable=W3301
    if args.xlim:
        ax.set_xlim(args.xlim[0], args.xlim[1])
    else:
        ax.set_xlim((xmin + xmax - smax) / 2, (xmin + xmax + smax) / 2)
    if args.ylim:
        ax.set_ylim(args.ylim[0], args.ylim[1])
    else:
        ax.set_ylim((ymin + ymax - smax) / 2, (ymin + ymax + smax) / 2)
    if args.zlim:
        ax.set_zlim(args.zlim[0], args.zlim[1])
    else:
        ax.set_zlim((zmin + zmax - smax) / 2, (zmin + zmax + smax) / 2)
    ax.set_box_aspect([1, 1, 1])

    if args.scale and args.scale > 0:
        if args.dgram:
            ax.plot([xmax - args.scale, xmax], [ymin - smax / 10, ymin - smax / 10], [zmin, zmin],
                    color='k', linewidth=3)
        else:
            ax.plot([xmax - args.scale, xmax], [ymin, ymin], [zmin, zmin],
                    color='k', linewidth=3)
            ax.plot([xmax, xmax], [ymin, ymin + args.scale], [zmin, zmin],
                    color='k', linewidth=3)
            ax.plot([xmax, xmax], [ymin, ymin], [zmin, zmin + args.scale],
                    color='k', linewidth=3)

    plt.show() if not args.out else plt.savefig(args.out, dpi=100)
