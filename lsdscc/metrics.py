import collections
import numpy as np
import logging

import lsdscc.align as _align

_logger = logging.getLogger(__name__)

LSDSCCScore = collections.namedtuple('LSDSCCScore', ['mds', 'pds', 'max_bleu'])

__all__ = [
    "LSDSCCScore",
    "compute_score_on_hypothesis_set",
]


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


def compute_score_on_hypothesis_set(hypothesis_set, annotated_refs, aligner=None):
    alignment = set()
    max_bleu_list = []

    for h_i, h in enumerate(hypothesis_set):
        bleu_scores = [_multi_bleu(h, ref_corpus, aligner) for ref_corpus in annotated_refs]
        k = np.argmax(bleu_scores)
        _logger.info('hypothesis %d is aligned to ref_group %d', h_i, k)
        alignment.add(k)
        max_bleu = max(bleu_scores)
        max_bleu_list.append(max_bleu)

    mds = len(alignment) / len(annotated_refs)
    total_ref_len = sum(len(ref) for ref in annotated_refs)
    pds = sum(len(annotated_refs[k]) for k in alignment) / total_ref_len
    max_bleu = np.mean(max_bleu_list)
    return LSDSCCScore(mds, pds, max_bleu)


def compute_score_on_hypothesis_corpus(): pass
