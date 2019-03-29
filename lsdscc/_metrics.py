import collections
import nltk.translate.bleu_score as bleu
from nltk.translate.bleu_score import SmoothingFunction
import numpy as np
import bleu.metrics as our_bleu

LSDSCCScore = collections.namedtuple('LSDSCCScore', ['mds', 'pds', 'max_bleu'])

_chencherry = SmoothingFunction()


def _multi_bleu(hypothesis_sentence, reference_corpus):
    """
    Encapsulate the BLEU variant we use.

    :param hypothesis_sentence:
    :type hypothesis_sentence: List[str]
    :param reference_corpus:
    :type reference_corpus: List[List[str]]
    :return: The BLEU score.
    """
    return bleu.sentence_bleu(
        references=reference_corpus,
        hypothesis=hypothesis_sentence,
        smoothing_function=_chencherry.method4,
    )


def compute_score_on_hypothesis_set(hypothesis_set, annotated_refs):
    alignment = set()
    max_bleu_list = []

    for h in hypothesis_set:
        bleu_scores = [_multi_bleu(h, ref_corpus) for ref_corpus in annotated_refs]
        k = np.argmax(bleu_scores)
        alignment.add(k)
        max_bleu = max(bleu_scores)
        max_bleu_list.append(max_bleu)

    mds = len(alignment) / len(annotated_refs)
    total_ref_len = sum(len(ref) for ref in annotated_refs)
    pds = sum(len(annotated_refs[k]) for k in alignment) / total_ref_len
    max_bleu = np.mean(max_bleu_list)
    return LSDSCCScore(mds, pds, max_bleu)


def compute_score_on_hypothesis_corpus(): pass
