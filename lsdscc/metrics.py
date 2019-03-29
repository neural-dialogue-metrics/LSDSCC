import collections
import logging

import numpy as np

import lsdscc.align as _align

__all__ = [
    "LSDSCCScore",
    "HypothesisSet",
    "ReferenceSet",
    "compute_score_on_hypothesis_set",
    "compute_score_on_hypothesis_corpus",
]

_logger = logging.getLogger(__name__)

LSDSCCScore = collections.namedtuple('LSDSCCScore', ['mds', 'pds', 'max_bleu'])


class HypothesisSet:
    """
    This a simple wrapper of a list of sentence representing the hypothesis set.
    This class makes the headache of thinking of deeply-nested list less killing.
    """

    def __init__(self, hypothesis_sentences):
        self._hypothesis_sentences = hypothesis_sentences
        pass

    def __iter__(self):
        return iter(self._hypothesis_sentences)

    def __len__(self):
        """
        Return the number of hypotheses in the set.

        :return:
        """
        return len(self._hypothesis_sentences)

    def __getitem__(self, item):
        return self._hypothesis_sentences[item]

    def __str__(self):
        return "\n".join("%d: %r" % (i, h) for i, h in enumerate(self._hypothesis_sentences))

    def __repr__(self):
        return '<%s with %d sentences>' % (self.__class__.__name__, len(self))

    @classmethod
    def create_from_line(cls, line, eos=None):
        pass


class ReferenceSet:
    """
    This class represents a 2-level multiple reference group.
    """

    def __init__(self, annotated_refs):
        self._reference_set = annotated_refs

    def __len__(self):
        return len(self._reference_set)

    def __iter__(self):
        return iter(self._reference_set)

    def __getitem__(self, item):
        return self._reference_set[item]


def _multi_bleu(hypothesis_sentence, reference_corpus, aligner=None):
    """
    Encapsulate the BLEU variant we use.

    :param hypothesis_sentence:
    :type hypothesis_sentence: List[str]
    :param reference_corpus:
    :type reference_corpus: List[List[str]]
    :return: The BLEU score.
    """
    if aligner is None:
        aligner = _align.BleuAligner()
    return aligner(hypothesis_sentence, reference_corpus)


def compute_score_on_hypothesis_set(hypothesis_set, reference_set, aligner=None):
    alignment = set()
    max_bleu_list = []

    for h_i, h in enumerate(hypothesis_set):
        bleu_scores = [_multi_bleu(h, ref_corpus, aligner) for ref_corpus in reference_set]
        k = np.argmax(bleu_scores)
        _logger.info('hypothesis %d is aligned to ref_group %d', h_i, k)
        alignment.add(k)
        max_bleu = max(bleu_scores)
        max_bleu_list.append(max_bleu)

    mds = len(alignment) / len(reference_set)
    total_ref_len = sum(len(ref) for ref in reference_set)
    pds = sum(len(reference_set[k]) for k in alignment) / total_ref_len
    max_bleu = np.mean(max_bleu_list)
    return LSDSCCScore(mds, pds, max_bleu)


def compute_score_on_hypothesis_corpus(hypothesis_corpus, reference_corpus, aligner=None):
    assert len(hypothesis_corpus) == len(reference_corpus)
    score_values = []
    for hypothesis, annotated_refs in zip(hypothesis_corpus, reference_corpus):
        score = compute_score_on_hypothesis_set(hypothesis, annotated_refs, aligner)
        score_values.append(score)
    mean = np.mean(score_values, axis=0)
    return LSDSCCScore(*mean)
