"""Testing module tree."""

from treem import Tree


def test_tree_traversal():
    """Tests tree traversal."""
    tree0 = Tree()
    tree1 = tree0.add(Tree())
    tree2 = tree1.add(Tree())
    tree3 = tree1.add(Tree())
    pre = list(x for x in tree0.preorder())
    post = list(x for x in tree0.postorder())
    level = list(x for x in tree0.levelorder())
    assert pre == [tree0, tree1, tree2, tree3]
    assert post == [tree2, tree3, tree1, tree0]
    assert level == [tree3, tree2, tree1, tree0]
    assert tree0.depth() == 0
    assert tree1.depth() == 1
    assert tree2.depth() == 2
    assert tree3.depth() == 2
    assert tree2.width() == 2
    assert tree0.height() == 2
