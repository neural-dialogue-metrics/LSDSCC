import unittest
import os

from lsdscc.dataset import _load_dialogs
from lsdscc.dataset import _load_reference_groups
from lsdscc.dataset import DATASET_ZIP_FILE
from lsdscc.dataset import GROUP_FILE
from lsdscc.dataset import DATA_ROOT

from lsdscc.tests import TOTAL_DIALOGS
from lsdscc.tests import TOTAL_GROUPS


class TestLoadDataset(unittest.TestCase):

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
        groups = _load_reference_groups()
        self.assertEqual(len(groups), TOTAL_GROUPS)
