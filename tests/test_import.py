"""Import tests of the main module treem and it's submodules."""

# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel
# ruff: noqa: F401


def test_import_treem():
    """Tests importing treem."""
    import treem


def test_import_node():
    """Tests importing Node from treem."""
    from treem import Node


def test_import_morph():
    """Tests importing Morph from treem."""
    from treem import Morph


def test_import_swc():
    """Tests importing SWC from treem."""
    from treem import SWC


def test_import_geom():
    """Tests importing geom utils from treem."""
    from treem.utils.geom import rotation_matrix
    from treem.utils.geom import norm
    from treem.utils.geom import angle_between
    from treem.utils.geom import rotation
    from treem.utils.geom import repair_branch
    from treem.utils.geom import sample


def test_import_plot():
    """Tests importing plot utils from treem."""
    from treem.utils.plot import plot_tree
    from treem.utils.plot import plot_section
    from treem.utils.plot import plot_neuron
    from treem.utils.plot import plot_points
