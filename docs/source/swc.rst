SWC specification
=================

The SWC data format specification used by the ``treem`` package.

Format
------

- Plain-text file with 7-column tabular data (one node per line).
- Lines starting with ``#`` are comments (ignored).
- Structure: ``<I> <T> <X> <Y> <Z> <R> <P>``

+-------+--------+----------------+----------------------------------------+
| Field | Column | Description    | Values                                 |
+=======+========+================+========================================+
| I     | 0      | Node ID        | int: 1 (root), 2, 3, ...               |
+-------+--------+----------------+----------------------------------------+
| T     | 1      | Point type     | int: 1 (soma), 2 (axon), 3 (dend), 4   |
|       |        |                | (apic)                                 |
+-------+--------+----------------+----------------------------------------+
| X/Y/Z | 2/3/4  | Coordinates    | float (micrometers)                    |
+-------+--------+----------------+----------------------------------------+
| R     | 5      | Radius         | float (micrometers)                    |
+-------+--------+----------------+----------------------------------------+
| P     | 6      | Parent node ID | int: -1 (parent of root), 1, 2, ...    |
+-------+--------+----------------+----------------------------------------+

Rules
-----

1. Node IDs:

   - Start at 1, increment sequentially by 1.
   - Unique, positive integers.

2. Root:

   - Exactly one root: ``I=1``, ``T=1``, ``P=-1``.

3. Parent-child:

   - All non-root nodes have only one parent and ``P < I`` (no loops).
   - Parent IDs must exist in the file, except ``P=-1`` for root.

4. Soma (type 1, ``T=1``):

   - Must be represented as one of the following:

     - Single node (root only).
     - Single section starting from the root.
     - Two sections from root (e.g., 3-point soma).

5. Non-somatic nodes (``T in {2,3,4}``):

   - Each non-soma branch (neurite) originates in root.
   - Non-soma branches must maintain consistent type ``P`` within a
     branch. First node of a neurite (stem) has parent root.

6. Validity:

   - File must have ``>=1`` data rows.
   - ``T in {1,2,3,4}``, other types invalidate the file.

Terminology
-----------

+-----------+----------------------------------------------------------+
| Term      | Definition                                               |
+===========+==========================================================+
| Tree      | Hierarchical structure with no loops. Each node has      |
|           | ``<=1``  parent.                                         |
+-----------+----------------------------------------------------------+
| Branch    | A maximal sub-tree of the same type ``P`` (a neurite).   |
+-----------+----------------------------------------------------------+
| Node      | Single SWC line (point in 3D).                           |
+-----------+----------------------------------------------------------+
| Root      | Node with no parent (``I=1``, ``T=1``, ``P=-1``).        |
+-----------+----------------------------------------------------------+
| Child     | Node with a parent.                                      |
+-----------+----------------------------------------------------------+
| Parent    | Node with ``>=1`` child.                                 |
+-----------+----------------------------------------------------------+
| Leaf      | Node with no children (``degree=0``).                    |
+-----------+----------------------------------------------------------+
| Fork      | Non-root node with ``>1`` child (``degree>1``).          |
|           | Bifurcation if ``degree=2``.                             |
+-----------+----------------------------------------------------------+
| Depth     | Ancestor count from root (root ``depth=0``).             |
+-----------+----------------------------------------------------------+
| Height    | Max edges from node to any leaf in its sub-tree.         |
+-----------+----------------------------------------------------------+
| Size      | Total nodes in (sub-)tree.                               |
+-----------+----------------------------------------------------------+
| Breadth   | Total leaves in (sub-)tree.                              |
+-----------+----------------------------------------------------------+
| Width     | Nodes at same depth as current node.                     |
+-----------+----------------------------------------------------------+
| Segment   | Line connecting two nodes (parent and child).            |
+-----------+----------------------------------------------------------+
| Section   | Continuous chain of segments between fork/root/leaf      |
|           | nodes.                                                   |
+-----------+----------------------------------------------------------+
| Stem      | First node of non-somatic branch.                        |
+-----------+----------------------------------------------------------+
