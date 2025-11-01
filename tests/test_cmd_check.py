"""Testing CLI command check."""

import subprocess
import os


def test_no_file():
    """Tests for missing file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_no_file.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, _ = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'no_file: fail_no_file.swc\n'


def test_no_data():
    """Tests for empty file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_no_data.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'no_data: True\n'
    assert stderr == ''


def test_node1_has_parent():
    """Tests whether first node is root."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_node1_has_parent.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 3
    assert stdout == """node1_has_parent: 2
non_stem_neurite: 2
not_valid_parent_ids: 2
"""
    assert stderr == ''


def test_node1_not_id1():
    """Tests whether first node has ID of 1."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_node1_not_id1.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 2
    assert stdout == """node1_not_id1: 2
non_stem_neurite: 3
"""
    assert stderr == ''


def test_node1_not_soma():
    """Tests whether first node has TYPE of 1."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_node1_not_soma.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 2
    assert stdout == """node1_not_soma: 3
non_stem_neurite: 1
"""
    assert stderr == ''


def test_non_descendant():
    """Tests whether node ID is greater than parent ID."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_non_descendant.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 2
    assert stdout == """non_stem_neurite: 2
non_descendant: 2 3
"""
    assert stderr == ''


def test_non_increasing_ids():
    """Tests whether IDs are increasing."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_non_increasing_ids.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'non_increasing_ids: 3 2\n'
    assert stderr == ''


def test_non_sequential_ids():
    """Tests whether ID increment is 1."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_non_sequential_ids.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'non_sequential_ids: 4 6\n'
    assert stderr == ''


def test_non_stem_neurite():
    """Tests for neurites changing type (e.g., axon from dend)."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_non_stem_neurite.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'non_stem_neurite: 4\n'
    assert stderr == ''


def test_non_unique_ids():
    """Tests for unique IDs."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_non_unique_ids.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 2
    assert stdout == """non_unique_ids: 2 3
non_increasing_ids: 2
"""
    assert stderr == ''


def test_not_array_1():
    """Tests for matrix shape of the data."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_not_array_1.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'not_array: True\n'
    assert stderr == ''


def test_not_array_2():
    """Tests for data matrix contains numbers."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_not_array_2.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'not_array: True\n'
    assert stderr == ''


def test_not_swc_cols():
    """Tests for data matrix has shape (N, 7)."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_not_swc_cols.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'not_swc_cols: 8\n'
    assert stderr == ''


def test_not_swc_ext():
    """Tests for data file name extension SWC."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_not_swc_ext.txt'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'not_swc_ext: txt\n'
    assert stderr == ''


def test_not_valid_ids():
    """Tests for valid IDs."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_not_valid_ids.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 2
    assert stdout == """not_valid_ids: 0 -1
non_increasing_ids: 0 -1
"""
    assert stderr == ''


def test_not_valid_parent_ids():
    """Tests for valid parent IDs."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_not_valid_parent_ids.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'not_valid_parent_ids: 4 5\n'
    assert stderr == ''


def test_not_valid_types():
    """Tests for valid point types."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_not_valid_types.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'not_valid_types: 6 5\n'
    assert stderr == ''


def test_single_point():
    """Tests for the number of data points greater than 1."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_single_point.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'single_point: 1\n'
    assert stderr == ''


def test_undef_parent_ids():
    """Tests for disconnected nodes."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_undef_parent_ids.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'undef_parent_ids: 3 4\n'
    assert stderr == ''


def test_unordered():
    """Tests unordered SWC file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'fail_unordered.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 5
    assert stdout == """node1_not_id1: 2
node1_has_parent: 1
node1_not_soma: 3
not_valid_parent_ids: 1
non_increasing_ids: 10 9 6 1 4
"""
    assert stderr == ''


def test_simple_branch(tmp_path):
    """Tests unordered SWC file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'check', 'pass_simple_branch.swc',
                             '-o', tmp_path / 'test_treem.json'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''
