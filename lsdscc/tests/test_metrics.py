import unittest
import pathlib
import json

import lsdscc.utils as utils

from lsdscc.metrics import max_bleu_score
from lsdscc.utils import make_ref_group
from lsdscc.dataset import EvalDataset
from lsdscc.utils import parse_response_file, run_all_metrics
from lsdscc._metrics import compute_score_on_hypothesis_set

DATA_ROOT = pathlib.Path(__file__).parent / 'data'
assert DATA_ROOT.is_dir()

QUERY_FILE = DATA_ROOT / 'query.txt'
RESPONSE_FILE = DATA_ROOT / 'response.txt'
GROUP_FILE = DATA_ROOT / 'groups.json'

N_RESPONSES = 8


class TestHypothesisSetLevel(unittest.TestCase):
    def test(self):
        with open(GROUP_FILE) as f:
            data = json.load(f)
        annotated_refs = utils.make_annotated_refs(data)[0][-1]
        hypothesis_set = parse_response_file(RESPONSE_FILE)
        hypothesis_set = hypothesis_set[0]
        score = compute_score_on_hypothesis_set(hypothesis_set, annotated_refs)
        print(score)
