"""
Implement the three metrics described in the paper LSDSCC: a Large Scale Domain-Specific Conversational Corpus for
Response Generation with Diversity Oriented Evaluation Metrics.

- MaxBLEU
- MDS
- PDS
"""
from nltk.translate.bleu_score import sentence_bleu
import numpy as np

__all__ = [
    "maxBLEU",
    "mean_diversity_score",
    "probabilistic_diversity_score",
]


def _compute_alignment(responses, reference_group):
    """
    Compute the alignment between the response set and the reference_group.
    Return a dict. The keys are id of response and the value is the id of a reference set.

    :param responses:
    :param reference_group:
    :return:
    """
    alignment = {response_id: _argmax_multi_bleu(response, reference_group)
                 for response_id, response in enumerate(responses)}
    return alignment


def mean_diversity_score(responses, reference_group):
    """
    Calculate the MDS (Mean Diversity Score) described by the paper.

    MDS is the percentage of members that align to at least one response in a reference_group.
    A member is said to *align to* a response if the maxBLEU of the response and the member yields
    the index of the member within its group. In other words, the member *has* the highest semantic relevance
    to the response within the group. Those special members are counted and then divided by the total number
    of member to yield the MDS score.

    :param responses: a list of sentences. A model can generate a set of responses w.r.t a query.
    These responses are evaluated as an entity on the degree of diversity.
    :param reference_group: a group of reference sets.
    :return: the MDS score.
    """
    alignment = _compute_alignment(responses, reference_group)
    overlap = len(set(alignment.values()))
    return len(alignment) / len(reference_group)


def probabilistic_diversity_score(responses, reference_group):
    """
    Calculate the PDS (Probabilistic Diversity Score) described by the paper.

    PDS is a weighted version of MDS that takes into account the number of references
    in each semantic group.
    :param responses: a list of sentences. A model can generate a set of responses w.r.t a query.
    These responses are evaluated as an entity on the degree of diversity.
    :param reference_group: a group of reference sets.
    :return: the PDS score.
    """
    alignment = _compute_alignment(responses, reference_group)
    overlap = set(alignment.values())
    numerator = sum(len(reference_group[k]) for k in overlap)
    denominator = sum(len(refs) for refs in reference_group)
    return numerator / denominator


def _multi_bleu(response, reference_group):
    return [sentence_bleu(refs, response,
                          emulate_multibleu=True) for refs in reference_group]


def _argmax_multi_bleu(response, reference_group):
    """
    Calculate MaxBLEU described by the paper.

    MaxBLEU is the foundation of MDS and PDS and it is based on multi-BLEU.
    multi-BLEU measures the semantic relevance between a single sentence response
    and multiple reference sentences. The reference_group is a list of such multiple-references
    so it is a list-of-list.

    The MaxBLEU is computed as follow:

    1. multi-BLEU(response, references) is computed for each multiple references in the group.
    2. The group that yields the maximum score is taken as the winner.
    3. The index of the winner is returned.

    :param responses: a sentence.
    :param reference_group: a list of multiple references, each is a list of sentences.
    :return: the index of the group that has the highest semantic relevance to the response.
    """
    return np.argmax(_multi_bleu(response, reference_group))


def maxBLEU(responses, reference_group):
    return np.mean(
        np.max(_multi_bleu(response, reference_group))
        for response in responses
    )
