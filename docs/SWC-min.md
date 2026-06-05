# SWC File Specification

## Format
- Plain-text file with 7-column tabular data (one node per line).
- Lines starting with '#' are comments (ignored).
- Structure: '<I> <T> <X> <Y> <Z> <R> <P>'

| Field | Column | Description       | Values                     |
|-------|--------|-------------------|----------------------------|
| I     | 0      | Node ID           | int: 1 (root), 2, 3, ...   |
| T     | 1      | Point type        | int: 1 (soma), 2 (axon), 3 (dend), 4 (apic) |
| X/Y/Z | 2/3/4  | Coordinates       | float (um)                 |
| R     | 5      | Radius            | float (um)                 |
| P     | 6      | Parent node ID    | int: -1 (parent of root), 1, 2, ...  |

---

## Rules
1. Node IDs:
   - Start at 1, increment sequentially by 1.
   - Unique, positive integers.

2. Root:
   - Exactly one root: 'I=1', 'T=1', 'P=-1'.

3. Parent-Child:
   - All non-root nodes have one parent ('P < I').
   - Parent IDs must exist in the file (except 'P=-1' for root).

4. Soma (Type 1):
   - Must be one of:
     - Single node (root).
     - Single branch from root.
     - Two branches from root (e.g., 3-point soma).

5. Non-Somatic Nodes (Types 2/3/4):
   - Must have 'P=1' if directly connected to root.
   - Type must match parent's type (unless parent is root).

6. Validity:
   - File must have >=2 data rows.
   - 'T in {1, 2, 3, 4}' (other types ignored).

---

## Terminology
| Term         | Definition                                                                                     |
|--------------|------------------------------------------------------------------------------------------------|
| Tree         | Hierarchical structure with no loops. Each node has <=1 parent.                                |
| Node         | Single SWC line (point in 3D).                                                                 |
| Root         | Node with no parent ('I=1', 'T=1', 'P=-1').                                                  |
| Child        | Node with a parent.                                                                           |
| Parent       | Node with >=1 child.                                                                            |
| Leaf         | Node with no children (degree=0).                                                             |
| Fork         | Non-root node with >1 child (degree>1). Bifurcation if degree=2.                              |
| Depth        | Ancestor count from root (root depth=0).                                                      |
| Height       | Max edges from node to any leaf in its sub-tree.                                              |
| Size         | Total nodes in (sub-)tree.                                                                    |
| Breadth      | Total leaves in (sub-)tree.                                                                    |
| Width        | Nodes at same depth as current node.                                                          |
| Segment      | Geometric frustum between parent/child nodes.                                                 |
| Section      | Tree portion between structural points (root/fork/leaf).                                     |
| Stem         | First non-somatic node (Type 2/3/4) directly descending from root.                            |
