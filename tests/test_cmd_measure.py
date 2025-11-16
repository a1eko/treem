"""Testing CLI command measure."""

import os
import subprocess


def test_measure():
    """Tests for morphometric mesurements."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'measure', 'pass_simple_branch.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    # same base radius if parent is root
    assert stdout == """pass_simple_branch
dend area        19.7422
dend breadth           3
dend contrac           1
dend degree            2
dend diam          0.382
dend dist        8.48528
dend length      16.9706
dend nbranch           2
dend nstem             1
dend nterm             3
dend order             3
dend seclen      3.39411
dend volume      1.90866
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


def test_out(tmp_path):
    """Tests for writing to file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'measure', 'pass_simple_branch.swc',
                             '-o', tmp_path / 'test_treem.json'],
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
