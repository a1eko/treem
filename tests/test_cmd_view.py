"""Testing CLI command view."""

import subprocess
import os


def test_png(tmp_path):
    """Tests for common plot."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-o', tmp_path / 'test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_pdf(tmp_path):
    """Tests for plot options."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-t', 'title', '--no-axes', '--show-id',
                             '--scale', '100', '-c', 'cells',
                             '-b', '2', '-s', '4', '-m', '3', '9',
                             '-a', '20', '30',
                             '-o', tmp_path / 'test_treem.pdf'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_shadow(tmp_path):
    """Tests for plot options."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             'pass_zjump.swc', '-c', 'shadow',
                             '-o', tmp_path / 'test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_proj_xy(tmp_path):
    """Tests for plot projection."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-j', 'xy',
                             '-o', tmp_path / 'test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_proj_xz(tmp_path):
    """Tests for plot projection."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-j', 'xz',
                             '-o', tmp_path / 'test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_proj_yz(tmp_path):
    """Tests for plot projection."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-j', 'yz',
                             '-o', tmp_path / 'test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''
