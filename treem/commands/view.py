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

mpl.rcParams['axes.prop_cycle'] = cycler(color=_colors)


def _setup_matplotlib_and_axes(args):
    """Setup Matplotlib figure, 3D axes, and initial parameters."""
    plt.rc('font', size=args.font)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    # clean up 3D pane appearance
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.set_edgecolor('w')
        pane.fill = False
    ax.set_proj_type('ortho')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.grid(False)

    if args.title:
        fig.suptitle(args.title, fontsize=args.title_font)
    if args.no_axes:
        ax.set_axis_off()

    if args.cycler_color:
        colors = list(_colors)
        for x in args.cycler_color:
            i, colorname = x.split(':')
            i = int(i)
            if 0 <= i < _NCOLORS:
                colors[i] = colorname
        mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)

    return fig, ax


def _load_and_plot_morphology(ax, args, types):
    """Load and plot morphology data based on the selected mode."""
    morph = None

    for count, file_name in enumerate(reversed(args.file)):
        if not args.dgram:
            current_morph = Morph(file_name)
        else:
            current_morph = DGram(source=file_name, zorder=count,
                                  ystep=args.dgram_ystep, zstep=args.dgram_zstep, types=types)
        if args.mode == 'neurites':
            plot_neuron(ax, current_morph, types, linewidth=args.linewidth)
        elif args.mode == 'cells':
            colors = {k: f'C{count % _NCOLORS}' for k in types}
            plot_neuron(ax, current_morph, types, colors=colors, linewidth=args.linewidth)
        elif args.mode == 'shadow':
            if count > 0:  # shadow for all but the first (non-reversed) file
                colors = {k: args.shadow_color for k in types}
                plot_neuron(ax, current_morph, types, colors=colors,
                            linewidth=args.shadow_width)
            else:  # the main neuron (first in original args.file)
                plot_neuron(ax, current_morph, types, linewidth=args.linewidth)
        # the last morph object to be used for branch/sec/mark operations
        if count == 0:
            morph = current_morph
    return morph


def _plot_special_features(ax, args, morph, types):
    """Plot branches, sections, and marks."""
    if not morph:
        return

    nodes_to_plot = []
    if args.branch:
        groups = args.branch
        plot_func = plot_tree
    elif args.sec:
        groups = args.sec
        plot_func = plot_section
    else:
        groups = []
        plot_func = None

    if plot_func and groups:
        for group in groups:
            group_capture = group
            types_capture = types
            # find nodes that match group ID and type
            nodes = filter(lambda x, g=group_capture: x.ident() in g, morph.root.walk())
            nodes = filter(lambda x, t=types_capture: x.type() in t, nodes)
            nodes_to_plot.extend(list(nodes))
            for node in nodes_to_plot:
                plot_func(ax, node, morph.data,
                          linewidth=1.5 * args.linewidth, color='C5')
            if args.show_id:
                plot_points(ax, morph, group, types,
                            show_id=args.show_id, markersize=6 * args.linewidth)

    if args.mark:
        for group in args.mark:
            plot_points(ax, morph, group, types,
                        show_id=args.show_id, markersize=6 * args.linewidth)


def _set_view_and_limits(ax, args):
    """Set view angle, projection, axis limits, aspect ratio, and scale bar."""
    if args.angle:
        ax.view_init(args.angle[0], args.angle[1])

    if args.proj:
        if args.proj.lower() == 'xy':
            ax.view_init(89.99, -90.01)
            ax.set_zlabel(''); ax.set_zticks([])
        if args.proj.lower() == 'xz':
            ax.view_init(0.00, -90.01)
            ax.set_ylabel(''); ax.set_yticks([])
        if args.proj.lower() == 'yz':
            ax.view_init(0.00, 0.01)
            ax.set_xlabel(''); ax.set_xticks([])

    xmin, ymin = ax.xy_dataLim.xmin, ax.xy_dataLim.ymin
    xmax, ymax = ax.xy_dataLim.xmax, ax.xy_dataLim.ymax
    zmin, zmax = ax.zz_dataLim.xmin, ax.zz_dataLim.xmax
    # pylint: disable=W3301
    smax = max(max(ax.xy_dataLim.size), max(ax.zz_dataLim.size))

    # set limits for 1:1:1 aspect ratio
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
            # scale bar for DGram mode
            ax.plot([xmax - args.scale, xmax], [ymin - smax / 10, ymin - smax / 10], [zmin, zmin],
                    color='k', linewidth=3)
        else:
            # standard 3D scale bar (X, Y, Z axes)
            ax.plot([xmax - args.scale, xmax], [ymin, ymin], [zmin, zmin],
                    color='k', linewidth=3)
            ax.plot([xmax, xmax], [ymin, ymin + args.scale], [zmin, zmin],
                    color='k', linewidth=3)
            ax.plot([xmax, xmax], [ymin, ymin], [zmin, zmin + args.scale],
                    color='k', linewidth=3)


def view(args):
    """Display neuron morphology structure."""
    # pylint: disable=expression-not-assigned
    types = args.type if args.type else SWC.TYPES
    fig, ax = _setup_matplotlib_and_axes(args)
    morph = _load_and_plot_morphology(ax, args, types)
    _plot_special_features(ax, args, morph, types)
    _set_view_and_limits(ax, args)
    plt.show() if not args.out else plt.savefig(args.out, dpi=100)
