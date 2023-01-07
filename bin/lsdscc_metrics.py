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
