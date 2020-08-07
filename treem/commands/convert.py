"""Implementation of CLI convert command."""

import numpy as np

from treem import Node, SWC, Morph


def convert(args):
    """Converts input data to compliant SWC format."""
    vprint = print if not args.quiet else lambda *a, **k: None
    nam = 'I', 'T', 'X', 'Y', 'Z', 'R', 'P'
    fmt = 'i', 'i', 'f', 'f', 'f', 'f', 'i'
    try:
        data = np.loadtxt(args.file, dtype={'names': nam, 'formats': fmt})
        types = args.type if args.type else SWC.TYPES
        nodes = [Node(row) for row in data if row[SWC.T] in types
                 or row[SWC.P] == -1]
        root = [node for node in nodes if node.v[SWC.P] == -1][0]
        root.v[SWC.T] = SWC.SOMA
        for i, node in enumerate(nodes, 1):
            parent_id = node.v[SWC.P]
            for parent in nodes:
                if parent.v[SWC.I] == parent_id:
                    parent.add(node)
                    break
            vprint(f'converted {int(i/len(nodes)*100):>3d}%', end='\r')
        vprint()
        idmap = {-1: -1}
        for ident, node in enumerate(root.walk(), 1):
            idmap[node.v[SWC.I]] = ident
        for row in data:
            if row[SWC.T] in types or row[SWC.P] == -1:
                row[SWC.I], row[SWC.P] = idmap[row[SWC.I]], idmap[row[SWC.P]]
        data = np.array([node.v for node in root.walk()])
        Morph(data=data).save(args.out)
        return 0
    except (KeyError, IndexError, ValueError):
        vprint(f'can not convert {args.file}.')
        return 1
