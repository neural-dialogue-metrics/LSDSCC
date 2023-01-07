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

from .bleu import _bleu_without_bp


class BleuAligner:
    """
    An Aligner that uses the original BLEU with BP=1 and smoothing proposed by Lin et al. (2002).
    """

    def __init__(self, n=None):
        self.n = n

    def __call__(self, hypothesis_sentence, reference_corpus):
        return _bleu_without_bp(
            translation_corpus=[hypothesis_sentence],
            reference_corpus=[reference_corpus],
            smooth=True,
            max_order=self.n,
        )


class NLTKBleuAligner:
    """
    An Aligner that uses the ``nltk.translate.bleu_score.sentence_bleu``.
    """

    def __init__(self, smooth_function=None):
        import nltk.translate.bleu_score as bleu_score

        self._smooth_function = smooth_function
        self._sentence_bleu = bleu_score.sentence_bleu

    def __call__(self, hypothesis_sentence, reference_corpus):
        return self._sentence_bleu(
            references=reference_corpus,
            hypothesis=hypothesis_sentence,
            smoothing_function=self._smooth_function,
        )


class NLTKNistAligner:
    """
    An Aligner that uses the ``nltk.translate.nist_score.sentence_nist``.
    """

    def __init__(self, n=5):
        import nltk.translate.nist_score as nist_score

        self._sentence_nist = nist_score.sentence_nist
        self.n = n

    def __call__(self, hypothesis_sentence, reference_corpus):
        return self._sentence_nist(
            references=reference_corpus, hypothesis=hypothesis_sentence, n=self.n
        )
