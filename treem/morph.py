"""Morphology reconstruction data structure."""

import math

from collections import deque

import numpy as np

from treem.tree import Tree
from treem.io import SWC, load_swc, save_swc
from treem.utils.geom import rotation_matrix, norm


class Node(Tree):
    """Morphology data storage."""

    def __init__(self, value=None):
        """Inits Node with value."""
        super().__init__()
        self.v = value  # pylint: disable=invalid-name

    def __str__(self):
        """String representation of Node value."""
        return str(self.v)

    def walk(self, reverse=False):
        """Iterates through the tree nodes starting from the current node.

        Iteration is terminated when root is reached if reverse is
        True. If False, full tree is traversed downstream in pre-order.

        Args:
            reverse (bool): walk the tree in ascending order if True.

        Returns:
            sequence of tree nodes (generator object).
        """

        iterator = Tree.preorder if not reverse else Tree.ascendorder
        return iterator(self)

    def is_stem(self):
        """Returns True if node is a stem node."""
        return (not self.is_root() and self.parent.is_root() and self.type() is not SWC.SOMA)

    def order(self):
        """Returns branch order (int). A primary neurite has order 1."""
        one = 1 if not self.is_fork() else 0
        return (sum(1 for _ in self.forks(iterator=Tree.ascendorder)) + one
                if not self.is_root() else 0)

    def ident(self):
        """Returns node ID (int)."""
        return int(self.v[SWC.I])

    def parent_ident(self):
        """Returns node's parent ID (int)."""
        return int(self.v[SWC.P])

    def type(self):
        """Returns point type of the node (int)."""
        return int(self.v[SWC.T])

    def point(self):
        """Returns point data of the node (x,y,z,r) (NumPy ndarray[4])."""
        return self.v[SWC.XYZR]

    def coord(self):
        """Returns coordinates of the node (x,y,z) (NumPy ndarray[3])."""
        return self.v[SWC.XYZ]

    def dist(self, origin=[0.0, 0.0, 0.0]):  # pylint: disable=dangerous-default-value
        """Returns Euclidean distance of the node to origin (float)."""
        return np.linalg.norm(self.v[SWC.XYZ] - origin)

    def radius(self):
        """Returns radius of the node (float)."""
        return self.v[SWC.R]

    def diam(self):
        """Returns diameter of the node (float)."""
        return 2 * self.radius()

    def length(self):
        """Returns segment length at the node (float)."""
        # pylint: disable=invalid-name
        a = self.coord()
        b = self.parent.coord() if not self.is_root() else a
        return norm(a - b)

    def area(self):
        """Returns segment area at the node (float)."""
        # pylint: disable=invalid-name
        h = self.length()
        a = self.radius()
        b = self.parent.radius() if not self.is_root() else a
        return math.pi * (a + b) * math.sqrt((a - b) * (a - b) + h * h)

    def volume(self):
        """Returns segment volume at the node (float)."""
        # pylint: disable=invalid-name
        h = self.length()
        a = self.radius()
        b = self.parent.radius() if not self.is_root() else a
        return math.pi / 3.0 * (a * a + a * b + b * b) * h

    def section(self, reverse=False):
        """
        Iterates through the nodes of the section.

        Iteration starts with the current node and procedes until the
        end of the section.

        Args:
            reverse (bool): ascending order if True (defaults to False).

        Yields:
            sequence of nodes (generator object).
        """

        iterator = Tree.preorder if not reverse else Tree.ascendorder
        for node in iterator(self):
            yield node
            term = node if not reverse else node.parent
            if term.is_fork() or term.is_leaf() or term.is_root():
                break

    def sections(self):
        """Iterates through the sections in descending order.

           Iterations traverse entire branch starting with the current node.

           Yields:
               sequence of sections (generator object).
        """
        queue = deque((self.section(),))
        while queue:
            sec = list(queue.pop())
            node = sec[-1]
            siblings = deque(child.section() for child in node.siblings)
            queue.extend(reversed(siblings))
            yield sec


class Morph():
    """Neuron morphology representation."""

    def __init__(self, source=None, data=None):
        """Initializes Morph from source file or data.

        Args:
            source (str): source file (swc).
            data (NumPy ndarray): morphology data (N, 7).
        """
        self.data = None
        self.root = None
        self.nodes = []
        if source:
            self.load(source)
        elif data is not None:
            data[0][SWC.P] = -1
            idmap = dict(enumerate([int(x[0]) for x in data], 1))
            idmap = {v: k for k, v in idmap.items()}
            idmap[-1] = -1
            for rec in data:
                rec[SWC.I] = idmap[int(rec[SWC.I])]
                rec[SWC.P] = idmap[int(rec[SWC.P])]
            self.load(data=data)

    def load(self, source=None, data=None):
        """Fill-in Morph from source file or data.

        Args:
            source (str): source file (swc).
            data (NumPy ndarray): morphology data (N, 7).
        """
        self.data = load_swc(source) if source else data
        for row in self.data:
            self.nodes.append(Node(row))
        self.root = self.nodes[0]
        for node in self.nodes[1:]:
            parent = node.parent_ident() - 1
            child = node.ident() - 1
            self.nodes[parent].add(self.nodes[child])

    def save(self, target):
        """Writes morphology to file (str)."""
        save_swc(target, self.data)

    def node(self, ident):
        """Returns node by it's ID."""
        return [node for node in self.root.walk() if node.ident() == ident][0]

    def stems(self):
        """Iterates through stem nodes.

        Returns:
            sequence of stem nodes (generator object).
        """
        return filter(lambda x: x.type() != SWC.SOMA, self.root.siblings)

    def coords(self, sec):
        """Returns reference to section coordinates."""
        first = sec[0].ident() - 1
        last = sec[-1].ident()
        block = slice(first, last)
        return self.data[block, SWC.XYZ]

    def radii(self, sec):
        """Returns reference to section radii."""
        first = sec[0].ident() - 1
        last = sec[-1].ident()
        block = slice(first, last)
        return self.data[block, SWC.RADII]

    def points(self, sec):
        """Returns reference to section data."""
        first = sec[0].ident() - 1
        last = sec[-1].ident()
        block = slice(first, last)
        return self.data[block, SWC.XYZR]

    def length(self, sec):
        """Returns section length (float)."""
        return sum(node.length() for node in sec)

    def area(self, sec):
        """Returns section area (float)."""
        return sum(node.area() for node in sec)

    def volume(self, sec):
        """Returns section volume (float)."""
        return sum(node.volume() for node in sec)

    def move(self, shift, node):
        """Shifts node coordinates by 3D vector (float[3])."""
        node.v[SWC.XYZ] += shift

    def translate(self, shift, node=None):
        """Shifts coordinates of the branch at the given node.

        Branch is traversed downstream from the given node.

        Args:
            shift (float[3]): translation vector.
            node (treem.Node): starting node (defaults to root).
        """
        node = node if node else self.root
        for sec in node.sections():
            points = self.coords(sec)
            points += shift

    def rotate(self, axis, angle, node=None):
        """Rotates branch at the node.

        Branch is traversed downstream from the given node.

        Args:
            axis (float[3]): rotation axis.
            angle (float): rotation angle in degrees.
            node (treem.Node): starting node (defaults to root).
        """
        node = node if node else self.root
        head = node.coord().copy()
        for sec in node.sections():
            points = self.coords(sec)
            first = sec[0].ident() - 1
            last = sec[-1].ident()
            block = slice(first, last)
            self.data[block, SWC.XYZ] = np.dot(rotation_matrix(axis, angle),
                                               points.T).T
        shift = head - node.coord()
        self.translate(shift, node)

    def copy(self, node=None):
        """Copies branch at the node (defaults to root)."""
        node = node if node else self.root
        data = np.array([x.v for x in node.walk()])
        return Morph(data=data)

    # Programming notes:
    # 1) __renumber() changes internal container data;
    # 2) delete(), insert(), prune() and graft() desynchronize
    #    the data and the linked list;
    # 3) constructor Morph(data=new_data) updates the linked list.

    def __renumber(self):
        """Renumbers morphology nodes in tree traversal order."""
        data = np.array([x.v for x in self.root.walk()])
        idmap = dict(enumerate([int(x[0]) for x in data], 1))
        idmap = {v: k for k, v in idmap.items()}
        idmap[-1] = -1
        for rec in data:
            rec[SWC.I], rec[SWC.P] = idmap[rec[SWC.I]], idmap[rec[SWC.P]]
        self.data = data

    def delete(self, node):
        """Delete node."""
        siblings = node.parent.siblings
        index = siblings.index(node)
        siblings.pop(index)
        for child in node.siblings:
            node.parent.add(child)
            child.v[SWC.P] = node.parent.ident()
        self.__renumber()

    def insert(self, new_node, node):
        """Inserts new node before the given node."""
        siblings = node.parent.siblings
        index = siblings.index(node)
        siblings.pop(index)
        maxid = np.max(self.data[:, slice(SWC.I, SWC.I + 1)]).astype(int)
        new_node.v[SWC.I] = maxid + 1
        new_node.v[SWC.P] = node.parent.ident()
        node.v[SWC.P] = new_node.ident()
        node.parent.add(new_node)
        new_node.add(node)
        self.__renumber()

    def prune(self, node):
        """Prunes branch at the given node."""
        siblings = node.parent.siblings
        index = siblings.index(node)
        siblings.pop(index)
        self.__renumber()

    def graft(self, tree, node=None):
        """Grafts tree at the given node (defaults to root)."""
        node = node if node else self.root
        maxid = np.max(self.data[:, slice(SWC.I, SWC.I + 1)]).astype(int)
        tree.data[:, slice(SWC.I, SWC.P + 1, SWC.P)] += maxid
        tree.data[0][SWC.P] = node.ident()
        self.data = np.append(self.data, tree.data, axis=0)
        node.add(tree.root)
        self.__renumber()


def get_segdata(morph):
    """Collects extended segment data."""
    # pylint: disable=invalid-name
    # pylint: disable=too-many-locals
    m = morph
    d = {}
    for i, t, x, y, z, r, p in m.data:
        i, t, x, y, z, r, p = int(i), int(t), float(x), float(y), float(z), float(r), int(p)
        d[i] = {'t': t, 'x': x, 'y': y, 'z': z, 'r': r, 'p': p}
    center = m.root.coord()

    """
    for node in m.root.walk():
        if node.type() == SWC.SOMA:
            ident = node.ident()
            d[ident]['length'] = 0.0
            d[ident]['path'] = 0.0
            d[ident]['xsec'] = 0.0
            d[ident]['xsec_rel'] = 0.0
            d[ident]['dist'] = 0.0
            d[ident]['degree'] = 0
            d[ident]['order'] = 0
            d[ident]['breadth'] = 0
            d[ident]['totlen'] = 0.0
    """
    soma_idents = [node.ident() for node in m.root.walk() if node.type() == SWC.SOMA]
    for ident in soma_idents:
        ident = node.ident()
        d[ident].update({
                'length': 0.0,
                'path': 0.0,
                'xsec': 0.0,
                'xsec_rel': 0.0,
                'dist': 0.0,
                'degree': 0,
                'order': 0,
                'breadth': 0,
                'totlen': 0.0
                })

    # forward traversal
    for stem in m.stems():
        for sec in stem.sections():
            order = 1
            xsec = 0.0
            seclen = m.length(sec)
            for node in sec:
                ident = node.ident()
                length = node.length()
                xsec += length
                if node.parent.is_fork() and node.parent != m.root:
                    order = d[node.parent.ident()]['order'] + 1
                dist = np.linalg.norm(center - node.coord())
                path = d[node.parent.ident()]['path']
                path += length
                d[ident]['length'] = length
                d[ident]['path'] = path
                d[ident]['xsec'] = xsec
                d[ident]['xsec_rel'] = xsec / seclen
                d[ident]['dist'] = dist
                d[ident]['degree'] = node.degree()
                d[ident]['order'] = order
                d[ident]['breadth'] = 1
                d[ident]['totlen'] = 0.0

    # backward traversal
    for term in m.root.leaves():
        for node in term.walk(reverse=True):
            if not node.is_leaf():
                ident = node.ident()
                descent_ident = [x.ident() for x in node.siblings]
                descent_length = [x.length() for x in node.siblings]
                descent_breadth = [d[i]['breadth'] for i in descent_ident]
                descent_totlen = [d[i]['totlen'] for i in descent_ident]
                breadth = sum(descent_breadth)
                totlen = sum(descent_totlen) + sum(descent_length)
                d[ident]['breadth'] = breadth
                d[ident]['totlen'] = totlen

    return np.array([[i, d[i]['t'], d[i]['x'], d[i]['y'], d[i]['z'],
                      d[i]['r'], d[i]['p'],
                      d[i]['length'], d[i]['path'], d[i]['xsec'], d[i]['xsec_rel'],
                      d[i]['dist'], d[i]['degree'], d[i]['order'], d[i]['breadth'],
                      d[i]['totlen']]
                     for i in sorted(d)])


class SEG():  # pylint: disable=too-few-public-methods
    """Definitions of the extended segment data format."""
    (I, T, X, Y, Z, R, P, LENGTH, PATH, XSEC, XSEC_REL,
     DIST, DEGREE, ORDER, BREADTH, TOTLEN) = range(16)


class DGram(Morph):
    """Neuron dendrogram representation."""
    def __init__(self, morph=None, source=None, data=None, types=SWC.TYPES,
                 zorder=0.0, ystep=0.0, zstep=0.0):
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        if not morph:
            morph = Morph(source=source, data=data)
        else:
            morph = Morph(data=morph.data)
        if morph is None:
            super().__init__()
        else:
            for stem in morph.stems():
                if stem.type() not in types:
                    morph.prune(stem)
            graph = Morph(data=morph.data)
            segdata = get_segdata(graph)
            for sec in graph.root.sections():
                # mean section radius: secrad = graph.radii(sec).mean()
                for node in sec:
                    ident = node.ident()
                    data = graph.data[ident - 1]
                    segd = segdata[ident - 1]
                    data[SWC.X] = segd[SEG.PATH]
                    # mean section radius: data[SWC.R] = secrad
            if np.isclose(ystep, 0.0) or np.isclose(zstep, 0.0):
                maxdist = max(node.dist() for node in morph.root.leaves())
                ntips = sum(1 for _ in morph.root.leaves())
                dgram_step = maxdist / ntips
            ystep = ystep if not np.isclose(ystep, 0.0) else dgram_step
            zstep = zstep if not np.isclose(zstep, 0.0) else dgram_step
            graph.data[:, SWC.YZ] = [0.0, zorder * zstep]
            for stem in graph.stems():
                for sec in stem.sections():
                    start_node = sec[0]
                    parent = start_node.parent
                    shift = start_node.coord() - parent.coord()
                    graph.translate(-shift, start_node)
            for index, term in enumerate(graph.root.leaves(), start=1):
                pos = index * ystep
                for node in term.walk(reverse=True):
                    ident = node.ident()
                    value = graph.data[ident - 1]
                    if node.is_fork() or node.is_root():
                        pos = np.mean([x.coord()[1] for x in node.siblings])
                    value[SWC.Y] = pos
            super().__init__(data=graph.data)
