"""
Symbolic constants of data files.
"""
import pathlib

_parent = pathlib.Path(__file__).parent
TEST_GROUP_JSON = _parent / 'test.group.json'
TEST_QUERIES_TXT = _parent / 'test.queries.txt'
DATASET_ZIP = _parent / 'dataset.zip'
