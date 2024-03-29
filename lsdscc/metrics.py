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

import collections
import logging
import numpy as np

import lsdscc.align as _align

__all__ = [
    "LSDSCCScore",
    "compute_score_on_hypothesis_set",
    "compute_score_on_corpus",
]

_logger = logging.getLogger(__name__)

LSDSCCScore = collections.namedtuple("LSDSCCScore", ["mds", "pds", "max_bleu"])


def _multi_bleu(hypothesis, reference_set, aligner):
    """
    Compute a list of scores with the aligner.

    :param hypothesis: a single hypothesis.
    :param reference_set: a reference set.
    :param aligner: a callable to compute the semantic similarity of a hypothesis
    and a list of references.
    :return: List[float]
    """
    return [aligner(hypothesis, refs) for refs in reference_set]


def compute_score_on_hypothesis_set(hypothesis_set, reference_set, aligner=None):
    """
    Compute the three metrics on a hypothesis set.

    :param hypothesis_set: a hypothesis set.
    :param reference_set: a reference set.
    :param aligner: a callable to compute the semantic similarity of a hypothesis
    and a list of references.
    :return: LSDSCCScore.
    """
    if aligner is None:
        aligner = _align.BleuAligner()

    alignment = set()
    max_bleu_list = []

    for h_i, h in enumerate(hypothesis_set):
        bleu_scores = _multi_bleu(h, reference_set, aligner)
        k = np.argmax(bleu_scores)
        _logger.info("hypothesis %d is aligned to ref_group %d", h_i, k)
        alignment.add(k)
        max_bleu = max(bleu_scores)
        max_bleu_list.append(max_bleu)

    mds = len(alignment) / len(reference_set)
    total_ref_len = sum(len(refs) for refs in reference_set)
    pds = sum(len(reference_set[k]) for k in alignment) / total_ref_len
    max_bleu = np.mean(max_bleu_list)
    return LSDSCCScore(mds, pds, max_bleu)


def compute_score_on_corpus(hypothesis_corpus, reference_corpus, aligner=None):
    """
    Compute the three metrics on a corpus.
    This effectively compute the mean of scores of individual hypothesis sets.

    :param hypothesis_corpus: a list of hypothesis_set.
    :param reference_corpus: a list of reference_set.
    :param aligner: a callable to compute the semantic similarity of a hypothesis
    and a list of references.
    :return: LSDSCCScore.
    """
    assert len(hypothesis_corpus) == len(reference_corpus)
    score_values = []
    for hypothesis, annotated_refs in zip(hypothesis_corpus, reference_corpus):
        score = compute_score_on_hypothesis_set(hypothesis, annotated_refs, aligner)
        score_values.append(score)
    mean = np.mean(score_values, axis=0)
    return LSDSCCScore(*mean)
