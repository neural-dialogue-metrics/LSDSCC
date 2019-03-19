import unittest
from lsdscc.dataset import EvalDataset
from lsdscc.tests import TOTAL_GROUPS


class TestEvalDataset(unittest.TestCase):

    def test_create_from_pickle(self):
        dataset = EvalDataset.create_from_pickle()
        self.assertEqual(len(dataset.test_queries), TOTAL_GROUPS)

        group = dataset.get_reference_group(0)
        self.assertTrue(isinstance(group, list), msg='group is a list')
        self.assertTrue(isinstance(group[0], list), msg='subgroup is a list')
        self.assertTrue(isinstance(group[0][0], list), msg='reference is a list')
        self.assertTrue(isinstance(group[0][0][0], str), msg='token is a string')
