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
from lsdscc.metrics import compute_score_on_hypothesis_set
from lsdscc.metrics import compute_score_on_corpus
from lsdscc.ds import HypothesisSet, ReferenceSet
from lsdscc.tests.data import HYPOTHESIS_FILE, REFERENCE_FILE
from lsdscc.align import BleuAligner


class TestMetrics(unittest.TestCase):
    def test_compute_score_on_hypothesis_set(self):
        query = "they say star wars is about family conflict isn ' t it".split()
        hypothesis_set = [
            "i agree".split(),
            "remember the well known lyric from star wars ?".split(),
            "the new star wars series is coming out".split(),
            "and what about star war ii ?".split(),
            "can ' t agree more".split(),
            "go and watch star war".split(),
            "darth vader is cool".split(),
        ]

        reference_set = [
            [
                "totally agree".split(),
                "you r right , my family spent a good time watching it".split(),
            ],
            [
                "let ' s watch it once again".split(),
                "go and watch the new series".split(),
                "darth vader appears at the last scene of the new star war".split(),
            ],
        ]

        score = compute_score_on_hypothesis_set(hypothesis_set, reference_set)
        _score = compute_score_on_hypothesis_set(
            HypothesisSet(hypothesis_set), ReferenceSet(reference_set)
        )

        self.assertAlmostEqual(score.pds, _score.pds)
        self.assertAlmostEqual(score.mds, _score.mds)
        self.assertAlmostEqual(score.max_bleu, _score.max_bleu)

        print(score)

    def test_compute_score_on_corpus(self):
        hypothesis_corpus = HypothesisSet.load_corpus(HYPOTHESIS_FILE)
        reference_corpus = ReferenceSet.load_json_corpus(REFERENCE_FILE)
        score = compute_score_on_corpus(hypothesis_corpus, reference_corpus)
        print(score)
        _score = compute_score_on_corpus(
            hypothesis_corpus, reference_corpus, aligner=BleuAligner(n=5)
        )
        print(_score)
