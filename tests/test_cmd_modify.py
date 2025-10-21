"""Testing CLI command modify."""

import subprocess
import os


def test_scale(tmp_path):
    """Tests for scaling of dimensions."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_simple_branch.swc',
                             '-s', '1', '1', '1', '-e', '2',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_scale_radius(tmp_path):
    """Tests for scaling of radii."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_simple_branch.swc',
                             '-r', '1', '-b', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_unfold(tmp_path):
    """Tests for stretching and smoothing."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_zjump.swc',
                             '-t', '1', '-m', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_jitter(tmp_path):
    """Tests for node jittering."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_simple_branch.swc',
                             '-i', '2', '4', '8', '-j', '0.3',
                             '--seed', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_jitter_sec(tmp_path):
    """Tests for section jittering."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_simple_branch.swc',
                             '-i', '2', '4', '8', '-j', '0.3',
                             '--seed', '1', '--sec',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_twist(tmp_path):
    """Tests for branch twisting."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_simple_branch.swc',
                             '-i', '3', '9', '-w', '360',
                             '--seed', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_swap(tmp_path):
    """Tests for branch swapping."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_simple_branch.swc',
                             '-i', '4', '8', '-a',
                             '--seed', '1',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_prune(tmp_path):
    """Tests for branch pruning."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'modify', 'pass_simple_branch.swc',
                             '-i', '4', '8', '-u',
                             '-o', tmp_path / 'test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''
