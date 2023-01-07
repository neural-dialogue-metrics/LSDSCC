# MIT License
#
# Copyright (c) 2019 Cong Feng.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
from lsdscc.tests.data import REFERENCE_FILE, N_REF_SETS, N_REFERENCES
from lsdscc.ds import ReferenceSet

BUILTIN_N_REF_SETS = 299


class TestReferenceSet(unittest.TestCase):
    def test_from_json(self):
        json_dict = {
            "1": [
                "a",
            ],
            "2": [
                "a b",
            ],
            "3": [
                "a b c",
            ],
        }
        refset = [
            ["a".split()],
            ["a b".split()],
            ["a b c".split()],
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
        json_dict = {"null": ["a"], "1": ["a b"], "2": ["a b c"]}
        refset = [
            ["a b".split()],
            ["a b c".split()],
            ["a".split()],
        ]
        _refset = ReferenceSet.from_json(json_dict)
        self.assertEqual(refset, _refset._reference_set)
