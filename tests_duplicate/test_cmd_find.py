"""Testing CLI command find."""

import subprocess
import os


def test_all_nodes():
    """Tests for returning all nodes."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '1 2 3 4 5 6 7 8 9 10 11 12 13 \n'
    assert stderr == ''


def test_order():
    """Tests for nodes of the given branch order."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-e', '2'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    #assert stdout == '3 4 5 6 7 8 \n'
    assert stdout == '4 5 6 7 8 9 \n'
    assert stderr == ''


def test_order_sec():
    """Tests for sections of the given branch order."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-e', '2', '--sec'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '4 8 \n'
    assert stderr == ''


def test_breadth():
    """Tests for nodes of the given branch breadth."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-b', '1'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '4 5 6 7 10 11 12 13 \n'
    assert stderr == ''


def test_degree():
    """Tests for nodes of the given degree."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-g', '2'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '3 9 \n'
    assert stderr == ''


def test_stem():
    """Tests for stem starting nodes."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-e', '1', '--stem'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '2 \n'
    assert stderr == ''


def test_diam_gt():
    """Tests for diameter values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-d', '1'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '1 \n'
    assert stderr == ''


def test_diam_lt():
    """Tests for diameter values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-d', '0.1', '--comp', 'lt'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '5 \n'
    assert stderr == ''


def test_diam_eq():
    """Tests for diameter values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_simple_branch.swc',
                             '-d', '0.04', '--comp', 'eq'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '5 \n'
    assert stderr == ''


def test_length_gt():
    """Tests for length values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_zjump.swc',
                             '-l', '25'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '2 10 11 12 \n'
    assert stderr == ''


def test_length_lt():
    """Tests for length values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_zjump.swc',
                             '-l', '25', '--comp', 'lt'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '1 3 4 5 6 7 8 9 \n'
    assert stderr == ''


def test_length_eq():
    """Tests for length values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_zjump.swc',
                             '-l', '0.0', '--comp', 'eq'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '1 \n'
    assert stderr == ''


def test_zjump_gt():
    """Tests for zjump values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_zjump.swc',
                             '-z', '19'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '4 \n'
    assert stderr == ''


def test_zjump_lt():
    """Tests for zjump values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_zjump.swc',
                             '-z', '19', '--comp', 'lt'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '2 3 5 6 7 8 9 10 11 12 \n'
    assert stderr == ''


def test_zjump_eq():
    """Tests for zjump values."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_zjump.swc',
                             '-z', '20', '--comp', 'eq'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '4 \n'
    assert stderr == ''


def test_cut():
    """Tests for cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_nmo_2_cut.swc',
                             '-c', '10', '-p', '3'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '322 341 547 1167 \n'
    assert stderr == ''


def test_cut_bottom_up():
    """Tests for cut neurites."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'find', 'pass_nmo_3_cut.swc',
                             '-c', '10', '-p', '3', '--bottom-up'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == '521 1764 1848 1938 1956 1978 \n'
    assert stderr == ''
