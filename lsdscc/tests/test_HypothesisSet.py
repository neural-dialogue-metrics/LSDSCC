import unittest
from lsdscc.ds import HypothesisSet
from lsdscc.tests.data import RESPONSE_FILE, N_HYPOTHESES


class TestHypothesisSet(unittest.TestCase):

    def test_from_line(self):
        hs = HypothesisSet.from_line('a</s>b')
        self.assertEqual(list(hs), ['a'.split(), 'b'.split()])

        my_eos = r'<EOS>'
        hs = HypothesisSet.from_line(my_eos.join('ab'), eos=my_eos)
        self.assertEqual(list(hs), ['a'.split(), 'b'.split()])

    def test_load_corpus(self):
        corpus = HypothesisSet.load_corpus(RESPONSE_FILE)
        self.assertEqual(len(corpus), 1, msg='one element corpus')
        hs = corpus[0]
        self.assertEqual(len(hs), N_HYPOTHESES)
        print(hs)
        print(repr(hs))
