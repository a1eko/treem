"""Testing CLI command repair."""

import os
import subprocess


def test_transpose(tmp_path):
    """Tests for changing location."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-t', '2', '2', '2',
                             '-a', '90', '90', '90',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_shrink(tmp_path):
    """Tests for shrinkage correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-k', '1.33', '-kxy', '1.11', '-n',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_shrink_bottom_up(tmp_path):
    """Tests for shrinkage correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-k', '1.33', '-kxy', '1.11',
                             '--bottom-up',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_align(tmp_path):
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'align',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_split(tmp_path):
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'split',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_tilt(tmp_path):
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'tilt',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_zjump_join(tmp_path):
    """Tests for zjump correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_zjump.swc',
                             '-z', '4', '--zjump', 'join',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_joint(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'joint',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_joint_fail(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'fail_diam.swc',
                             '-d', '2', '--diam', 'joint',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == ''
    assert stderr == ''


def test_diam_sec(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'sec',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_order(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'order',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_order_pool(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'order',
                             '--pool', 'pass_zjump.swc',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_order_pool_err(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'order',
                             '--pool', 'pass_soma.swc',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == ''
    assert stderr == ''


def test_diam_breadth(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'breadth',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_breadth_pool(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'breadth',
                             '--pool', 'pass_zjump.swc',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_diam_breadth_pool_err(tmp_path):
    """Tests for diameter correction."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-d', '5', '--diam', 'breadth',
                             '--pool', 'pass_soma.swc',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == ''
    assert stderr == ''


def test_cut_repair(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_nmo_2_cut.swc',
                             '-c', '322', '341', '547', '1167',
                             '--seed', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_alt(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-c', '11', '13', '--seed', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_err(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-c', '7', '11', '13',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 3
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_err_force(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-c', '7', '11', '13',
                             '--force-repair',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 3
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_force(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch_2.swc',
                             '-c', '11', '13', '14', '--seed', '1',
                             '--force-repair',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_repair_pool(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_nmo_2_cut.swc',
                             '-c', '322', '341', '547', '1167',
                             '--pool', 'pass_nmo_1.swc',
                             '--seed', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_delete(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-l', '4', '8',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_cut_resample(tmp_path):
    """Tests for repairing cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'repair', 'pass_simple_branch.swc',
                             '-r', '0.5',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''
