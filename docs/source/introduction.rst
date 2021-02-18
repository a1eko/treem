
Introduction
============

Digital reconstructions of neuron morphology can be stored in different
binary or plain text data formats depending on the processing platform
or data repository (ASC, SWC, JSON and HDF5 to name a few).  The format
developed by Stockley, Wheal and Cannon, hence `SWC` (`Cannon et al.,
1998 <https://doi.org/10.1016/S0165-0270(98)00091-0>`_), is among the
oldest and most commonly recognized. Module ``treem`` deals exclusively
with reconstructions in SWC format.


.. rubric:: SWC File Format

An SWC file is a plain text file with metadata in '#'-comment lines,
usually placed in the header section, and the reconstruction data in
space-separated matrix. Each data line contains information from a single
measurement along the reconstructed neurite in seven fields::

    <I> <T> <X> <Y> <Z> <R> <P>

where the fields have the following meaning:

===== ====== ============== =========================
Field Column Description    Values
===== ====== ============== =========================
 I    0      Node ID        ``int``: 1, 2, ...
 T    1      Point type     ``int``: 1, 2, 3, 4 [...]
 X    2      `x` coordinate ``float`` (in micrometers)
 Y    3      `y` coordinate ``float`` (in micrometers)
 Z    4      `z` coordinate ``float`` (in micrometers)
 R    5      Radius         ``float`` (in micrometers)
 P    6      Parent node ID ``int``: -1, 1, 2, ...
===== ====== ============== =========================

The `node ID` is a unique identifier of each reconstructed point.
The `point type` is a user-defined flag denoting the specific part of the
neuron structure. It is not a required part of the structure definition
and there is no standard value format suggested by the authors. The
commonly used values of the point type agreed upon by most of the
developers are:

========== ==================================
Point type Corresponding cell part
========== ==================================
1          Soma
2          Axon
3          Dendrite in general (`e.g.` basal)
4          Apical dendrite, specifically
========== ==================================

One point in any file has a parent node ID of '-1', indicating it is the
`root` point, which is generally part of the soma. All other points have
one, and only one parent thus defining a topological `tree` structure
of the neuron morphology reconstruction.


.. rubric:: Tree Data Structure and Morphometry Terminology

Tree
    A tree is a hierarchical data structure where each element has
    no more than one parent to which it becomes a child. An element in
    the tree may link to one, several or no child elements. By definition,
    a tree has no loops.

Node
    An element of the tree. In ``treem``, each node contains the
    reconstruction data of a single row of SWC file.

Sub-tree, branch
    Part of a tree descendant of a given node of that tree.

Parent
    A node in the tree which has a further descendant sub-tree.

Child
    A node which has parent, is a child of the parent node.

Root
    A node which has no parent. Each tree has always one unique root node.

Siblings
    All nodes with the same parent.

Degree
    The total number of children of the given node.

Leaf, terminal, tip
    A node which has no children. A leaf has degree of 0.

Fork, branching point
    A node which has more than one child. A fork has degree higher than
    1. Forks with the degree of 2 are also called `bifurcation points`.

Depth, level
    The depth of a node is the number of connections from the root of
    the tree to that node.

Path
    A sequence of nodes in the descending order.

Height
    The total number of the nodes in the longest path of the tree,
    counted from the root.

Size
    The total number of the nodes in the tree.

Breadth
    The total number of the leaves of a given sub-tree.

Width
    The total number of the nodes of the same level as a given node.

Segment
    Geometrical part of the reconstructed neurite between the parent
    and the child nodes, `i.e.` a cone with the radius of the parent
    node at the base and the radius of the child node at the top. The
    height of the cone is the eucledian distance between the parent and
    the child nodes.

Section
    A part of the tree between two structural points (root, fork
    or leaf).

Stem
    The first non-somatic node of a section descendant to the root.

Tree traversal
    The method to visit all nodes of a tree. The tree traversal can be
    done in depth-first search order or breadth-first search order. The
    three forms of the deapth-first traversal are `in-order`, `pre-order`
    and `post-order`. The breadth-first traversal is `level-order`.
    For the recursive implementation of the above traversal algorithms
    see the ``treem.Tree`` code.


.. rubric:: Data Format Restrictions

Original SWC format is fairly flexible in its definition. The only strict
requirement is that the data has the uniform 7-field record length and
defines a topological tree structure. By design of the module ``treem``,
additional restrictions are imposed to standardize the data organisation
and speed up the processing.

* The input SWC file should have more than one data row. Comments and
  the metadata lines starting with the symbol '#' are ignored.

* Each data row should have 7 fields.

* The first node has ID of '1' and the parent ID of '-1', i.e. it is the
  root of the tree.

* The root node belongs to the soma.

* The point type could only be from the set '{1, 2, 3, 4}'.

* The node IDs of type ``int`` are unique and positive. ID of '0' is
  not defined.

* The parent IDs are a subset of the node IDs, except the parent ID of
  root, '-1'.

* The node IDs have the constant increment of '1'.

* The parent ID is always smaller than the node ID of a given node.

* The point type of the node is the same as the point type of its parent,
  unless the parent is root. Neurites of different types emerge from
  the soma and don't change their type.

