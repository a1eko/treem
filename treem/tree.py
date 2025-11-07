"""Basic tree data structure."""

from collections import deque


class Tree():
    """Recursive tree data structure."""

    def __init__(self):
        """Constructor of empty tree."""
        self.parent = None
        self.siblings = []

    def add(self, tree):
        """Appends tree as continuation."""
        tree.parent = self
        self.siblings.append(tree)
        return tree

    def is_root(self):
        """Returns True if tree has no parent."""
        return self.parent is None

    def is_fork(self):
        """Returns True for a branching point (except root)."""
        return len(self.siblings) > 1 and not self.is_root()

    def is_leaf(self):
        """Returns True for a terminal node."""
        return len(self.siblings) == 0

    def preorder(self):
        """Traverses tree in pre-order (depth first).

        Yields:
            sequence of tree nodes (generator object).
        """
        queue = deque((self,))
        while queue:
            node = queue.pop()
            queue.extend(reversed(node.siblings))
            yield node

    def postorder(self):
        """Traverses tree in post-order (breadth first).

        Yields:
            sequence of tree nodes (generator object).
        """
        queue = deque((self,))
        visited = set()
        while queue:
            node = queue[-1]
            if node not in visited:
                visited.add(node)
                queue.extend(reversed(node.siblings))
            else:
                queue.pop()
                yield node

    def levelorder(self):
        """Traverses tree in level-order (breadth first).

        Yields:
            sequence of tree nodes (generator object).
        """
        queue = deque((self,))
        visited = set()
        while queue:
            node = queue[-1]
            if node not in visited:
                visited.add(node)
                queue.extend(node.siblings)
            else:
                queue.pop()
                yield node

    def ascendorder(self):
        """Iterates tree nodes in ascending order until root is reached.

        Yields:
            sequence of tree nodes (generator object).
        """
        node = self
        while node is not None:
            yield node
            node = node.parent

    def leaves(self):
        """Iterates tree terminals.

        Returns:
            sequence of tree nodes (generator object).
        """
        return filter(Tree.is_leaf, self.preorder())

    def forks(self, iterator=preorder):
        """Iterates tree branching points.

        Args:
            iterator: iterator type (defaults to ``Tree.preorder``)

        Returns:
            sequence of tree nodes (generator object).
        """
        return filter(Tree.is_fork, iterator(self))

    def degree(self):
        """Returns node degree."""
        return len(self.siblings)

    def size(self):
        """Returns tree size."""
        return sum(1 for _ in self.preorder())

    def breadth(self):
        """Returns tree breadth."""
        return sum(1 for _ in self.leaves())

    def depth(self):
        """Returns node depth."""
        return sum(1 for _ in self.ascendorder()) - 1

    level = depth

    def height(self):
        """Returns tree height."""
        path = []
        node_depth = self.depth()
        for leaf in self.leaves():
            path.append(leaf.depth() - node_depth)
        return max(path)

    def width(self):
        """Returns tree width."""
        node_depth = self.depth()
        root = deque(self.ascendorder(), maxlen=1).pop()
        return sum(1 for node in root.preorder() if node.depth() == node_depth)
