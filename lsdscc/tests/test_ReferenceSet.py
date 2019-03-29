import unittest
from lsdscc.tests.data import REFERENCE_FILE, N_REF_SETS, N_REFERENCES
from lsdscc.ds import ReferenceSet

BUILTIN_N_REF_SETS = 299


class TestReferenceSet(unittest.TestCase):

    def test_from_json(self):
        json_dict = {
            '1': [
                'a',
            ],
            '2': [
                'a b',
            ],
            '3': [
                'a b c',
            ]
        }
        refset = [
            ['a'.split()],
            ['a b'.split()],
            ['a b c'.split()],
        ]
        _refset = ReferenceSet.from_json(json_dict)
        self.assertEqual(refset, _refset._reference_set)

    def test_load_json_corpus(self):
        corpus = ReferenceSet.load_json_corpus(REFERENCE_FILE)
        assert len(corpus) == 1
        refset = corpus[0]

        self.assertEqual(len(refset), N_REF_SETS)
        n_references = sum(len(refs) for refs in refset)
        self.assertEqual(n_references, N_REFERENCES)

        print(repr(refset))
        print(refset)

    def test_load_builtin_json_corpus(self):
        corpus = ReferenceSet.load_json_corpus()
        self.assertEqual(len(corpus), BUILTIN_N_REF_SETS)

    def test_null_proved(self):
        json_dict = {
            'null': ['a'],
            '1': ['a b'],
            '2': ['a b c']
        }
        refset = [
            ['a b'.split()],
            ['a b c'.split()],
            ['a'.split()],
        ]
        _refset = ReferenceSet.from_json(json_dict)
        self.assertEqual(refset, _refset._reference_set)
