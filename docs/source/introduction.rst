
Introduction
============

Digital reconstructions of neuron morphology can be stored in various
binary or plain-text data formats, depending on the processing platform
or data repository (e.g., ASC, SWC, JSON, or HDF5). Among these, the
format developed by Stockley, Wheal, and Cannon - known as ``SWC``
(`Cannon et al., 1998 <https://doi.org/10.1016/S0165-0270(98)00091-0>`_) -
is one of the oldest and most widely recognized. The module ``treem``
works exclusively with reconstructions in the SWC format.


.. rubric:: SWC File Format

An SWC file is a plain-text file that contains metadata in lines
beginning with the ``#`` character, typically in the header section,
and reconstruction data organized in a space-separated matrix. Each
data line represents a single measurement along the reconstructed
neurite and contains seven fields::

    <I> <T> <X> <Y> <Z> <R> <P>

The fields have the following meanings:

===== ====== ============== =========================
Field Column Description    Values
===== ====== ============== =========================
 I    0      Node ID        ``int``: 1, 2, ...
 T    1      Point type     ``int``: 1, 2, 3, 4 [...]
 X    2      `X` coordinate ``float`` (micrometers)
 Y    3      `Y` coordinate ``float`` (micrometers)
 Z    4      `Z` coordinate ``float`` (micrometers)
 R    5      Radius         ``float`` (micrometers)
 P    6      Parent node ID ``int``: -1, 1, 2, ...
===== ====== ============== =========================

The `Node ID` is a unique identifier of each reconstructed point.
The `Point type` is a user-defined flag that denotes a specific part of
the neuron’s structure. The original format specification does not
define standard point-type values, but most developers follow these
common conventions:

========== ==================================
Point type Corresponding cell part
========== ==================================
1          Soma
2          Axon
3          Dendrite (basal dendrite)
4          Apical dendrite
========== ==================================

One point in any file has a parent node ID of '-1', indicating it is the
`root` point, which is generally part of the soma. All other points have
one, and only one parent thus defining a topological `tree` structure
of the neuron morphology reconstruction.


.. rubric:: Tree Data Structure and Morphometry Terminology

Tree
    A tree is a hierarchical data structure in which each element has
    at most one parent, to which it is considered a child. Each element
    may have one, several, or no child elements. By definition, a tree
    contains no loops.

Node
    A single element of the tree. In ``treem``, each node contains the
    reconstruction data corresponding to one row in an SWC file.

Sub-tree, branch
    A part of the tree that descends from a specific node.

Parent
    A node that has one or more child nodes.

Child
    A node that has a parent node and is considered its descendant.

Root
    A node which has no parent. Each tree has always one unique root node.

Siblings
    All child nodes of the same parent.

Degree
    The total number of children that a given node has.

Leaf, terminal, tip
    A node which has no children. A leaf has a degree of 0.

Fork, branching point
    A node which has more than one child. A fork has a degree greater than
    1. Forks with a degree of 2 are also called `bifurcation points`.

Depth, level
    The depth of a node is the number of connections between the root of
    the tree and that node.

Path
    A sequence of nodes traversed in descending order from parent to child.

Height
    The total number of nodes in the longest path of the tree,
    counted from the root.

Size
    The total number of nodes in the tree.

Breadth
    The total number of leaves in a given sub-tree.

Width
    The total number of the nodes at the same level as a given node.

Segment
    The geometric portion of a reconstructed neurite located between a
    parent and its child node. It can be represented as a cone with the
    radius of the parent node at the base and the radius of the child
    node at the top. The height of the cone corresponds to the Euclidean
    distance between the parent and child nodes.

Section
    A portion of the tree located between two structural points
    (root, fork, or leaf).

Stem
    The first non-somatic node of a section descending from the root.

Tree traversal
    A method for visiting all nodes of a tree. Traversal can be performed
    in either depth-first search (DFS) or breadth-first search (BFS)
    order. The three forms of depth-first traversal are `in-order`,
    `pre-order`, and `post-order`, while breadth-first traversal is
    referred to as `level-order`. For recursive implementations of these
    traversal algorithms, see the ``treem.Tree`` source code.


.. rubric:: Data Format Restrictions

The original SWC format is fairly flexible in its definition. The only
strict requirement is that the data maintain a uniform seven-field record
length and represent a topological tree structure. In the design of the
``treem`` module, additional restrictions are introduced to standardize
data organization and improve processing efficiency.

* The input SWC file must contain more than one data row. Comment and
metadata lines that begin with the ``#`` symbol are ignored.

* Each data row must contain seven fields.

* The first node must have an ID of ``1`` and a parent ID of ``-1``;
  in other words, it represents the root of the tree.

* The root node corresponds to the soma.

* The point type must belong to the set ``{1, 2, 3, 4}``.

* Node IDs (of type ``int``) must be unique and positive. An ID of ``0``
  is not defined.

* Parent IDs must form a subset of the node IDs, except for the parent
  ID of the root, which is ``-1``.

* Node IDs must increase sequentially by a constant increment of ``1``.

* The parent ID of a node must always be smaller than its own node ID.

* The point type of a node must match the point type of its parent,
  unless the parent is the root. Neurites of different types emerge
  from the soma and retain their type along their branches.
