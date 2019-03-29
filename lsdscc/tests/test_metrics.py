import json
import logging
import pathlib
import unittest

import lsdscc.ds as utils
from lsdscc.metrics import compute_score_on_hypothesis_set
from lsdscc.ds import load_response_corpus

DATA_ROOT = pathlib.Path(__file__).parent / 'data'
assert DATA_ROOT.is_dir()

QUERY_FILE = DATA_ROOT / 'query.txt'
RESPONSE_FILE = DATA_ROOT / 'response.txt'
GROUP_FILE = DATA_ROOT / 'groups.json'

N_RESPONSES = 8

logging.basicConfig(level=logging.INFO)


class TestHypothesisSetLevel(unittest.TestCase):
    def test(self):
        with open(GROUP_FILE) as f:
            data = json.load(f)
        annotated_refs = utils.make_annotated_refs(data)[0][-1]
        hypothesis_set = load_response_corpus(RESPONSE_FILE)
        hypothesis_set = hypothesis_set[0]
        self.assertEqual(N_RESPONSES, len(hypothesis_set))
        score = compute_score_on_hypothesis_set(hypothesis_set, annotated_refs)
        print(score)
