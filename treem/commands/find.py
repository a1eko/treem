"""Implementation of CLI find command."""

import numpy as np

from treem.morph import Morph
from treem.io import SWC
from treem.utils.geom import fibonacci_sphere
from treem.utils.geom import rotation_matrix
from treem.utils.geom import rotation


def _apply_comparison_filter(nodes, value, compare_mode, accessor):
    """Applies a comparison filter (gt, lt, eq) on nodes using an accessor function."""
    if value is None:
        return nodes

    if compare_mode == 'gt':
        return filter(lambda x: accessor(x) > value, nodes)
    elif compare_mode == 'lt':
        return filter(lambda x: accessor(x) < value, nodes)
    elif compare_mode == 'eq':
        return filter(lambda x: accessor(x) == value, nodes)
    
    return nodes


def _find_cuts_simple(nodes, morph, args):
    """Finds cut points using a simple Z-axis distance threshold."""
    nodes = filter(lambda x: x.is_leaf(), nodes)
    
    # Determine the Z-extreme based on the bottom_up flag
    if not morph.root.walk():
        return nodes
        
    if not args.bottom_up:
        zcut = max(x.coord()[SWC.Z] for x in morph.root.walk())
        return filter(lambda x: x.coord()[SWC.Z] > zcut - args.cut, nodes)
    else:
        zcut = min(x.coord()[SWC.Z] for x in morph.root.walk())
        return filter(lambda x: x.coord()[SWC.Z] < zcut + args.cut, nodes)


def _find_cuts_complex(nodes, morph, args):
    """Finds cut points using rotation and projection onto a fibonacci sphere."""
    
    node_list = list(filter(lambda x: x.is_leaf(), nodes))
    if not node_list:
        return []
        
    found_cuts = []
    points = fibonacci_sphere(args.cut_iter)
    ztip = np.array([x.v for x in node_list])
    zdir = (0, 0, 1)

    for vdir in points:
        vtip = ztip.copy()
        axis, angle = rotation(zdir, vdir)
        rotm = rotation_matrix(axis, angle)
        # Apply rotation to XYZ coordinates
        vtip[:, SWC.XYZ] = np.dot(rotm, vtip[:, SWC.XYZ].T).T
        
        # Calculate cuts based on Z-projection
        zmax = vtip[:, SWC.Z].max()
        cuts = [int(v[SWC.I]) for v in vtip if zmax - v[SWC.Z] < args.cut]
        found_cuts.append(cuts)
        
    # Find the set of cuts with the maximum number of nodes
    if not found_cuts:
        return []
        
    max_cuts = max(len(x) for x in found_cuts)
    final_cuts = next(cuts for cuts in found_cuts if len(cuts) == max_cuts)

    return filter(lambda x: x.ident() in final_cuts, node_list)


def find(args):
    """Locates single nodes in morphology reconstruction."""
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-locals
    
    # 1. Initialization and Basic Filters
    morph = Morph(args.file)
    types = args.type if args.type else SWC.TYPES
    nodes = filter(lambda x: x.type() in types, morph.root.walk())

    if args.nodes:
        nodes = filter(lambda x: x.ident() in args.nodes, nodes)
    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)
    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)
    if args.degree:
        nodes = filter(lambda x: x.degree() in args.degree, nodes)

    # 2. Comparison Filters (Diam, Length, Dist, Slice, Jump)
    
    # Diam filter
    nodes = _apply_comparison_filter(nodes, args.diam, args.compare, lambda x: x.diam())
    
    # Length filter
    nodes = _apply_comparison_filter(nodes, args.length, args.compare, lambda x: x.length())
    
    # Distance from root filter
    nodes = _apply_comparison_filter(nodes, args.dist, args.compare, lambda x: x.dist(morph.root.coord()))
    
    # Z-Slice filter
    nodes = _apply_comparison_filter(nodes, args.slice, args.compare, lambda x: x.coord()[SWC.Z])
    
    # Z-Jump filter (requires special accessor lambda)
    # The accessor lambda is more complex here to handle the is_root() check and difference calculation
    if args.jump is not None:
        def jump_accessor(x):
            if x.is_root():
                return -1 # Use a value that won't match any jump condition
            return abs((x.parent.coord() - x.coord())[SWC.Z])
            
        nodes = _apply_comparison_filter(nodes, args.jump, args.compare, jump_accessor)

    # 3. Cut Logic
    if args.cut:
        if not args.cut_find:
            nodes = _find_cuts_simple(nodes, morph, args)
        else:
            nodes = _find_cuts_complex(nodes, morph, args)

    # 4. Section and Stem Filters
    if args.sec:
        nodes = filter(lambda x: x.parent.is_fork() or x.parent.is_root(), nodes)

    if args.stem:
        stems = []
        # Convert filter object to list to allow iteration
        for node in list(nodes):
            stems.extend(x for x in filter(lambda x: x.is_stem() and x.type() != SWC.SOMA, node.walk(reverse=True))
                         if x not in stems)
        nodes = stems

    # 5. Output
    for node in nodes:
        print(node.ident(), end=' ')
    print()
