"""Testing module io."""

import json

import numpy as np
import pytest

from treem.io import TreemEncoder, load_swc, save_swc


class MyObject:
    def __init__(self, value):
        self.value = value

def test_io_encoder_success():
    """Tests JSON encoder for successful serialization."""
    data = [[1, 2, 3], np.array(range(4, 7)), {7, 8, 9}, 0, "a", {"a": 1, "1": "a"}]
    assert json.dumps(data, cls=TreemEncoder) == \
        '[[1, 2, 3], [4, 5, 6], [8, 9, 7], 0, "a", {"a": 1, "1": "a"}]'

def test_io_encoder_fallback_failure():
    """Tests that the encoder falls back to the parent and correctly raises TypeError."""
    custom_obj = MyObject(0)
    with pytest.raises(TypeError):
        json.dumps(custom_obj, cls=TreemEncoder)


SWC_DATA = np.array([
    [1, 1, 0.0, 0.0, 0.0, 1.0, -1],
    [2, 3, 5.0, 0.0, 0.0, 1.0, 1],
    [3, 3, 10.0, 0.0, 0.0, 0.5, 2]
], dtype=float)


def test_save_swc_format(tmp_path):
    """Tests save_swc."""
    target_file = tmp_path / "test_save.swc"
    save_swc(target_file, SWC_DATA)
    assert target_file.is_file()
    with open(target_file, 'r') as f:
        content = f.read().strip().split('\n')
    assert len(content) == len(SWC_DATA)
    first_line_parts = content[0].split()
    assert first_line_parts[0] == '1' # ID
    assert first_line_parts[1] == '1' # Type
    assert first_line_parts[-1] == '-1' # Parent_ID
    assert len(first_line_parts) == 7


def test_load_swc_content(tmp_path):
    """Tests load_swc."""
    target_file = tmp_path / "test_load.swc"
    save_swc(target_file, SWC_DATA)
    loaded_data = load_swc(target_file)
    assert loaded_data.shape == SWC_DATA.shape
    np.testing.assert_array_almost_equal(loaded_data, SWC_DATA)
