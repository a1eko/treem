"""Testing CLI command convert."""

import subprocess
import os


def test_unordered():
    """Tests for converting unordered SWC file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'convert', 'fail_unordered.swc',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    _, stderr = proc.communicate()
    assert proc.returncode == 0
    # assert stdout == ''
    assert stderr == ''


def test_not_array():
    """Tests for converting incorrect file."""
    os.chdir(os.path.dirname(__file__) + '/data')
    proc = subprocess.Popen(['swc', 'convert', 'fail_not_array_1.swc',
                             '-o', '/tmp/test_treem.swc'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    assert proc.returncode == 1
    assert stdout == 'cannot convert fail_not_array_1.swc.\n'
    assert stderr == ''
