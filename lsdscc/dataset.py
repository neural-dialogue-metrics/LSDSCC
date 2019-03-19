"""Handle dataset loading."""
import os
import json
import zipfile
import collections

__all__ = ["Dataset"]

DATA_ROOT = os.path.join(os.path.dirname(__file__), 'data')
GROUP_FILE = os.path.join(DATA_ROOT, 'test.group.json')
DATASET_ZIP_FILE = os.path.join(DATA_ROOT, 'dataset.zip')
DATASET_TXT = 'dataset.txt'

_QUERY_RESPONSE_SEPARATOR = '<EOS>#TAB#'


def _load_groups():
    with open(GROUP_FILE) as f:
        return json.load(f)


def _load_dialogs():
    with zipfile.ZipFile(DATASET_ZIP_FILE) as dataset_zip:
        with dataset_zip.open(DATASET_TXT) as f:
            raw_data = f.read().decode()
    return [line.split(_QUERY_RESPONSE_SEPARATOR) for line in raw_data.splitlines()]


class Dataset(collections.namedtuple('Dataset', 'dialogs groups')):
    @classmethod
    def create(cls):
        return cls(
            dialogs=_load_dialogs(),
            groups=_load_groups(),
        )
