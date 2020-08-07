"""Testing CLI command measure."""

import subprocess
import os


def test_measure():
    """Tests for morphometric mesurements."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'measure', 'pass_simple_branch.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == """pass_simple_branch
dend area        24.0904
dend breadth           3
dend contrac           1
dend degree            2
dend diam          0.382
dend length      16.9706
dend nbranch           2
dend nstem             1
dend nterm             3
dend order             3
dend seclen      3.39411
dend volume      3.56734
dend xdim              8
dend ydim              5
dend zdim              0
soma area        12.5664
soma diam              2
soma volume      4.18879
soma xroot             0
soma yroot             0
soma zroot             0\n
"""
    assert stderr == ''


def test_out():
    """Tests for writing to file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'measure', 'pass_simple_branch.swc',
                             '-o', '/tmp/test_treem.json'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_soma():
    """Tests for morphometric mesurements."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'measure', 'pass_soma.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout != ''
    assert stderr == ''
