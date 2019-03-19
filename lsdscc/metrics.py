"""
Implement the three metrics described in the paper LSDSCC: a Large Scale Domain-Specific Conversational Corpus for
Response Generation with Diversity Oriented Evaluation Metrics.

- MaxBLEU
- MDS
- PDS
"""
from nltk.translate.bleu_score import sentence_bleu
import numpy as np


def _compute_alignment(responses, reference_group):
    # The i-th response is aligned to the alignment[i]-th reference group.
    # By *aligned to* we mean in plain words, the response is semantically similar to the group.
    # Note the group is a cluster of semantically similar references.
    # In other words, ``max_bleu(responses[i], reference_group) == alignment[i]``
    alignment = set(max_bleu(response, reference_group) for response in responses)
    return alignment


def mean_diversity_score(responses, reference_group):
    """
    Calculate the MDS (Mean Diversity Score) described by the paper.

    MDS is the percentage of members that align to at least one response in a reference_group.
    A member is said to *align to* a response if the max_bleu of the response and the member yields
    the index of the member within its group. In other words, the member *has* the highest semantic relevance
    to the response within the group. Those special members are counted and then divided by the total number
    of member to yield the MDS score.

    :param responses: a list of sentences. A model can generate a set of responses w.r.t a query.
    These responses are evaluated as an entity on the degree of diversity.
    :param reference_group: a group of reference sets.
    :return: the MDS score.
    """
    alignment = _compute_alignment(responses, reference_group)
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
    numerator = sum(k * len(reference_group[k]) for k in alignment)
    denominator = sum(len(refs) for refs in reference_group)
    return numerator / denominator


def max_bleu(response, reference_group):
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

    :param response: a sentence.
    :param reference_group: a list of multiple references, each is a list of sentences.
    :return: the index of the group that has the highest semantic relevance to the response.
    """
    bleu_values = [sentence_bleu(refs, response,
                                 emulate_multibleu=True) for refs in reference_group]
    return np.argmax(bleu_values)


def cluster_response_sentences(responses, reference_group):
    """
    Cluster a list of responses according to their semantic similarity to the members of a group.
    This procedure can help understand and interpret the result of PDS and MDS.

    :param responses: a list of sentences.
    :param reference_group: a reference group.
    :return: a dictionary. key is the cluster number, also being the number of a member of the group.
    value is a list of responses belonging to this cluster.
    """
    clusters = {k: [] for k in range(len(reference_group))}
    for response in responses:
        k = max_bleu(response, reference_group)
        clusters[k].append(response)
    return clusters
