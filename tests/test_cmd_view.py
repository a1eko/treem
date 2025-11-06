"""Testing CLI command view."""

import subprocess
import os


def test_png():
    """Tests for common plot."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-o', '/tmp/test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_pdf():
    """Tests for plot options."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-t', 'title', '--no-axes', '--show-id',
                             '--scale', '100', '-c', 'cells',
                             '-b', '2', '-s', '4', '-m', '3', '9',
                             '-a', '20', '30',
                             '-o', '/tmp/test_treem.pdf'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_shadow():
    """Tests for plot options."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             'pass_zjump.swc', '-c', 'shadow',
                             '-o', '/tmp/test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_proj_xy():
    """Tests for plot projection."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-j', 'xy',
                             '-o', '/tmp/test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_proj_xz():
    """Tests for plot projection."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-j', 'xz',
                             '-o', '/tmp/test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''


def test_proj_yz():
    """Tests for plot projection."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'view', 'pass_simple_branch.swc',
                             '-j', 'yz',
                             '-o', '/tmp/test_treem.png'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 0
    assert stdout == ''
    assert stderr == ''
