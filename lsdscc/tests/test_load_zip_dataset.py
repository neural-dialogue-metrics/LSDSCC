import unittest
import os

from lsdscc.dataset import _load_dialogs
from lsdscc.dataset import _load_groups
from lsdscc.dataset import DATASET_ZIP_FILE
from lsdscc.dataset import GROUP_FILE
from lsdscc.dataset import DATA_ROOT

TOTAL_DIALOGS = 738095
TOTAL_GROUPS = 299


class TestLoadZipDataset(unittest.TestCase):

    def test_files_exist(self):
        self.assertTrue(os.path.isdir(DATA_ROOT))
        self.assertTrue(os.path.exists(DATASET_ZIP_FILE))
        self.assertTrue(os.path.exists(GROUP_FILE))

    def test_load_dialogs(self):
        dialogs = _load_dialogs()
        self.assertEqual(len(dialogs), TOTAL_DIALOGS)
        for item in dialogs:
            self.assertEqual(len(item), 2, msg='must be a query-response pair')

        sample = dialogs[0]
        print('A sample data point:')
        print('query: %s' % sample[0])
        print('response: %s' % sample[1])

    def test_load_groups(self):
        groups = _load_groups()
        self.assertEqual(len(groups), TOTAL_GROUPS)
