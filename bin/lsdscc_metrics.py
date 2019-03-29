import logging
import argparse
from lsdscc import HypothesisSet, ReferenceSet
from lsdscc import compute_score_on_corpus

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluate diversity oriented metrics of LSDSCC')
    parser.add_argument('hypothesis_file', help='file containing responses to be evaluated')
    parser.add_argument('--eos', '-e', help='end-of-sentence indicator to use in the response file')
    parser.add_argument('--reference_file', '-r', help='custom reference corpus to use. (in json format)')
    args = parser.parse_args()

    hypothesis_corpus = HypothesisSet.load_corpus(args.hypothesis_file, args.eos)
    reference_corpus = ReferenceSet.load_json_corpus(args.reference_file)
    score = compute_score_on_corpus(hypothesis_corpus, reference_corpus)

    print('MaxBLEU: %f' % score.max_bleu)
    print('MDS: %f' % score.mds)
    print('PDS: %f' % score.pds)
