- An SWC file represents the 3D structural skeleton of a neuron.
- An SWC file is a plain-text file.
- Lines beginning with # character are comment lines and should be ignored.
- Each data line contains seven fields defining a point in 3D reconstruction (a node)::

    <I> <T> <X> <Y> <Z> <R> <P>

- The data fields have the following meanings:

===== ====== ============== =========================
Field Column Description    Values
===== ====== ============== =========================
 I    0      Node ID        int: 1, 2, ...
 T    1      Point type     int: 1, 2, 3, 4 [...]
 X    2      X coordinate   float (micrometers)
 Y    3      Y coordinate   float (micrometers)
 Z    4      Z coordinate   float (micrometers)
 R    5      Radius         float (micrometers)
 P    6      Parent node ID int: -1, 1, 2, ...
===== ====== ============== =========================

- Node ID is a unique identifier for each reconstructed point, always starts with 1.
- Point type denotes a specific part of the neuron's structure.

========== ==================================
Point type Corresponding neuron part
========== ==================================
1          soma
2          axon
3          dend (basal dendrite)
4          apic (apical dendrite)
========== ==================================

- Root is the point with Node ID 1, Point type 1 (soma) and Parent ID -1.
- There is only one root in SWC file.
- All non-root points have one, and only one, parent.
- Tree data structure and morphometry terminology::

Tree data structure and morphometry terminology::

Tree
    A tree is a hierarchical data structure in which each element has
    at most one parent, to which it is considered a child. Each element
    may have one, several, or no child elements. By definition, a tree
    contains no loops.

Node
    A single element of the tree, defined in one line of an SWC file.

Sub-tree, branch
    A part of the tree that descends from a specific node.

Parent
    A node that has one or more child nodes.

Child
    A node that has a parent node and is considered its descendant.

Root
    A node which has no parent. Each tree has always one unique root node. 
    In an SWC file, the root must always have Node ID 1 and Point type 1 (soma).

Siblings
    All child nodes of the same parent.

Degree
    The total number of children that a given node has.

Leaf, terminal, tip
    A node which has no children. A leaf has a degree of 0.

Fork, branching point
    A non-root node which has more than one child. A fork has a degree 
    greater than 1. Forks with a degree of 2 are called *bifurcation points*.

Depth, level
    The depth of a node is the total number of ancestor connections 
    separating it from the absolute root of the tree. It is calculated by 
    counting the total nodes in its upward parental lineage minus one.

Path
    A sequence of nodes traversed in descending order from parent to child.

Height
    The maximum number of connections (edges) between the current node and 
    any leaf in its sub-tree, calculated as the maximum difference in depth 
    between those leaves and the current node.

Size
    The total number of nodes contained within the tree or sub-tree, calculated 
    by counting all elements traversed during a pre-order traversal.

Breadth
    The total number of leaf nodes contained within the tree or sub-tree.

Width
    The total number of nodes in the entire tree that share the exact same 
    depth (level) as the current node.

Segment
    The geometric portion of a reconstructed neurite located between a
    parent and its child node. It can be represented as a truncated cone (a
    frustum) with the radius of the parent node at the base and the radius
    of the child node at the top. The height of the frustum corresponds
    to the Euclidean distance between the parent and child nodes.

Section
    A portion of the tree located between two structural points
    (*root*, *fork*, or *leaf*).

Stem
    The first non-somatic node (Type 2, 3, or 4) of a section descending 
    directly from the root of the tree (Node ID 1).

- Additional restrictions to improve processing efficiency::

* The input SWC file must contain more than one data row.

* The point type must belong to the set {1, 2, 3, 4}. Lines with other
  point types are ignored.

* Node IDs must be integer, unique and positive.

* Parent IDs must form a subset of the node IDs, except for the parent
  ID of the root, which is -1.

* Node IDs must increase sequentially by a constant increment of 1.

* The parent ID of a node must always be smaller than its own node ID.

* The soma (Type 1) must be structured in one of three ways:
  1. A single node (the root).
  2. A single non-bifurcating branch starting at the root.
  3. Exactly two non-bifurcating branches both originating directly at
     the root.  The simplest case is three-point soma: one root node
     and two other nodes each connected to the root.

* The point type of a node must match the point type of its parent,
  unless the parent is the root (Node ID 1). Consequently, all non-somatic 
  stems (Types 2, 3, and 4) must have a Parent ID of 1. Non-somatic sections 
  must retain their specific type along all subsequent downstream branches.

