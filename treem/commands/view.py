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

# set default linewidth: mpl.rcParams['lines.linewidth'] = 1.0
# set default font size: mpl.rcParams.update({'font.size': 8})
mpl.rcParams['axes.prop_cycle'] = cycler(color=_colors)


def _setup_figure(args):
    """Sets up the Matplotlib figure, axes, and initial styles."""
    plt.rc('font', size=args.font)
    fig = plt.figure(figsize=(8, 8))
    # pylint: disable=invalid-name
    ax = fig.add_subplot(projection='3d')
    # basic axis style cleanup
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
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
    return fig, ax


def _apply_color_cycler(args):
    """Applies custom colors to the plot cycle."""
    if args.cycler_color:
        colors = list(_colors)
        for x in args.cycler_color:  # pylint: disable=invalid-name
            i, colorname = x.split(':')
            i = int(i)
            if 0 <= i < _NCOLORS:
                colors[i] = colorname
        mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)


def _load_and_plot_morphology(args, ax, types):
    """Loads morphology data and plots the main structure based on mode."""
    morph = None

    # helper to load Morph or DGram
    def _get_morph(file_name, count=None):
        if not args.dgram:
            return Morph(file_name)
        return DGram(source=file_name, zorder=count, ystep=args.dgram_ystep,
                     zstep=args.dgram_zstep, types=types)

    if args.mode == 'neurites':
        for count, file_name in enumerate(reversed(args.file)):
            morph = _get_morph(file_name, count)
            plot_neuron(ax, morph, types, linewidth=args.linewidth)
    elif args.mode == 'cells':
        for count, file_name in enumerate(reversed(args.file)):
            morph = _get_morph(file_name, count)
            colors = {k: f'C{count % _NCOLORS}' for k in types}
            plot_neuron(ax, morph, types, colors=colors, linewidth=args.linewidth)
    elif args.mode == 'shadow':
        # plot shadow files first
        for file_name in reversed(args.file[1:]):
            shadow_morph = _get_morph(file_name)
            colors = {k: args.shadow_color for k in types}
            plot_neuron(ax, shadow_morph, types, colors=colors,
                        linewidth=args.shadow_width)
        # plot main file last
        if args.file:
            morph = _get_morph(args.file[0])
            plot_neuron(ax, morph, types, linewidth=args.linewidth)
    # return the last plotted morphology object for subsequent overlays
    return morph


def _plot_overlays(args, ax, morph, types):
    """Plots optional overlays like branches, sections, and marked points."""
    if morph is None:
        return

    # common logic for branch and section plotting
    def _plot_overlay_nodes(groups, plotter_func):
        if not groups:
            return
        for group in groups:
            nodes = filter(lambda x, g=group: x.ident() in g, morph.root.walk())
            nodes = filter(lambda x: x.type() in types, nodes)
            for node in nodes:
                plotter_func(ax, node, morph.data,
                             linewidth=1.5 * args.linewidth, color='C5')
                if args.show_id:
                    plot_points(ax, morph, group, types,
                                show_id=args.show_id, markersize=6 * args.linewidth)
    _plot_overlay_nodes(args.branch, plot_tree)
    _plot_overlay_nodes(args.sec, plot_section)
    if args.mark:
        for group in args.mark:
            plot_points(ax, morph, group, types,
                        show_id=args.show_id, markersize=6 * args.linewidth)


def _configure_view_limits(args, ax):
    """Sets the camera angle, projection, and axis limits/aspect ratio."""
    if args.angle:
        ax.view_init(args.angle[0], args.angle[1])
    if args.proj:
        proj_map = {
            'xy': (89.99, -90.01, ax.set_zlabel, ax.set_zticks, []),
            'xz': (0.00, -90.01, ax.set_ylabel, ax.set_yticks, []),
            'yz': (0.00, 0.01, ax.set_xlabel, ax.set_xticks, []),
        }
        proj_key = args.proj.lower()
        if proj_key in proj_map:
            angle_a, angle_b, set_label_func, set_ticks_func, tick_list = proj_map[proj_key]
            ax.view_init(angle_a, angle_b)
            set_label_func('')
            set_ticks_func(tick_list)
    # calculate initial data limits
    xmin = ax.xy_dataLim.xmin
    ymin = ax.xy_dataLim.ymin
    zmin = ax.zz_dataLim.xmin
    xmax = ax.xy_dataLim.xmax
    ymax = ax.xy_dataLim.ymax
    zmax = ax.zz_dataLim.xmax
    # pylint: disable=W3301
    smax = max(max(ax.xy_dataLim.size), max(ax.zz_dataLim.size))
    # set X/Y/Z limits
    lims = {
        'x': (args.xlim, ax.set_xlim, xmin, xmax),
        'y': (args.ylim, ax.set_ylim, ymin, ymax),
        'z': (args.zlim, ax.set_zlim, zmin, zmax),
    }
    for axis, (arg_lim, set_lim_func, min_val, max_val) in lims.items():
        if arg_lim:
            set_lim_func(arg_lim[0], arg_lim[1])
        else:
            set_lim_func((min_val + max_val - smax) / 2, (min_val + max_val + smax) / 2)
    ax.set_box_aspect([1, 1, 1])


def _plot_scale_bar(args, ax, xmax, ymin, zmin, smax):
    """Plots the 3D scale bar."""
    if args.scale and args.scale > 0:
        if args.dgram:
            # DGram scale bar
            ax.plot([xmax - args.scale, xmax], [ymin - smax / 10, ymin - smax / 10], [zmin, zmin],
                    color='k', linewidth=3)
        else:
            # 3D scale bar (X, Y, Z axes)
            ax.plot([xmax - args.scale, xmax], [ymin, ymin], [zmin, zmin],
                    color='k', linewidth=3)
            ax.plot([xmax, xmax], [ymin, ymin + args.scale], [zmin, zmin],
                    color='k', linewidth=3)
            ax.plot([xmax, xmax], [ymin, ymin], [zmin, zmin + args.scale],
                    color='k', linewidth=3)


def view(args):
    """Display neuron morphology structure."""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=expression-not-assigned

    _, ax = _setup_figure(args)
    _apply_color_cycler(args)
    types = args.type if args.type else SWC.TYPES

    morph = _load_and_plot_morphology(args, ax, types)
    _plot_overlays(args, ax, morph, types)
    _configure_view_limits(args, ax)
    
    ymin = ax.xy_dataLim.ymin
    zmin = ax.zz_dataLim.xmin
    xmax = ax.xy_dataLim.xmax
    smax = max(max(ax.xy_dataLim.size), max(ax.zz_dataLim.size))
    _plot_scale_bar(args, ax, xmax, ymin, zmin, smax)

    plt.show() if not args.out else plt.savefig(args.out, dpi=100)
