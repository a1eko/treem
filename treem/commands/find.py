"""Implementation of CLI find command."""

from treem.morph import Morph
from treem.io import SWC


def find(args):  # pylint: disable=too-many-branches
    """Locates single nodes in morphology reconstruction."""
    morph = Morph(args.file)
    types = args.type if args.type else SWC.TYPES
    nodes = filter(lambda x: x.type() in types, morph.root.walk())
    if args.order:
        nodes = filter(lambda x: x.order() in args.order, nodes)
    if args.breadth:
        nodes = filter(lambda x: x.breadth() in args.breadth, nodes)
    if args.degree:
        nodes = filter(lambda x: x.degree() in args.degree, nodes)
    if args.stem:
        nodes = filter(lambda x: x.is_stem() and x.type() != SWC.SOMA, nodes)
    if args.diam is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: x.diam() > args.diam, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: x.diam() < args.diam, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: x.diam() == args.diam, nodes)
    if args.length is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: x.length() > args.length, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: x.length() < args.length, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: x.length() == args.length, nodes)
    if args.dist is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: x.dist() > args.dist, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: x.dist() < args.dist, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: x.dist() == args.dist, nodes)
    if args.jump is not None:
        if args.compare == 'gt':
            nodes = filter(lambda x: not x.is_root()
                           and abs((x.parent.coord()-x.coord())[2])
                           > args.jump, nodes)
        elif args.compare == 'lt':
            nodes = filter(lambda x: not x.is_root()
                           and abs((x.parent.coord()-x.coord())[2])
                           < args.jump, nodes)
        elif args.compare == 'eq':
            nodes = filter(lambda x: not x.is_root()
                           and abs((x.parent.coord()-x.coord())[2])
                           == args.jump, nodes)
    if args.cut:
        nodes = filter(lambda x: x.is_leaf(), nodes)
        if not args.bottom_up:
            zcut = max(x.coord()[2] for x in morph.root.walk())
            nodes = filter(lambda x: x.coord()[2] > zcut - args.cut, nodes)
        else:
            zcut = min(x.coord()[2] for x in morph.root.walk())
            nodes = filter(lambda x: x.coord()[2] < zcut + args.cut, nodes)

    if args.sec:
        nodes = filter(lambda x: x.parent.is_fork()
                       or x.parent.is_root(), nodes)

    for node in nodes:
        print(node.ident(), end=' ')
    print()
