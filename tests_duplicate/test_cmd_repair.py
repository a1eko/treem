"""Testing CLI command repair."""

import subprocess
import os


def test_transpose():
    """Tests for changing location."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-t', '2', '2', '2',
                             '-a', '90', '90', '90',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_shrink():
    """Tests for shrinkage correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-k', '1.33', '-kxy', '1.11', '-n',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_shrink_bottom_up():
    """Tests for shrinkage correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-k', '1.33', '-kxy', '1.11',
                             '--bottom-up',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_align():
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'align',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_split():
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'split',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_tilt():
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'tilt',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_join():
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'join',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_joint():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'joint',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_joint_fail():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'fail_diam.swc',
                             '-d', '2', '--diam', 'joint',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == ''
    assert stderr == ''


def test_diam_sec():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'sec',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_order():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'order',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_order_pool():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'order',
                             '--pool', 'pass_zjump.swc',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_order_pool_err():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'order',
                             '--pool', 'pass_soma.swc',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == ''
    assert stderr == ''


def test_diam_breadth():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'breadth',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_breadth_pool():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'breadth',
                             '--pool', 'pass_zjump.swc',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_breadth_pool_err():
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'breadth',
                             '--pool', 'pass_soma.swc',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == ''
    assert stderr == ''


def test_cut_repair():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_nmo_2_cut.swc',
                             '-c', '322', '341', '547', '1167',
                             '--seed', '1',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_alt():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-c', '11', '13', '--seed', '1',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_err():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-c', '7', '11', '13',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 3
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_err_force():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-c', '7', '11', '13',
                             '--force-repair',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 3
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_force():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch_2.swc',
                             '-c', '11', '13', '14', '--seed', '1',
                             '--force-repair',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_pool():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_nmo_2_cut.swc',
                             '-c', '322', '341', '547', '1167',
                             '--pool', 'pass_nmo_1.swc',
                             '--seed', '1',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_delete():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-l', '4', '8',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_resample():
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-r', '0.5',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''
