"""
Symbolic constants of data files.
"""
import pathlib

_parent = pathlib.Path(__file__).parent
default_reference_set = _parent / 'test.group.json'
TEST_QUERIES_TXT = _parent / 'test.queries.txt'
DATASET_ZIP = _parent / 'dataset.zip'
