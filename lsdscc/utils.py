import lsdscc.metrics as _lsdscc_metrics
from lsdscc.dataset import EvalDataset as _EvalDataset
import logging
import collections
import numpy as np

_logger = logging.getLogger(__name__)
DEFAULT_EOS = '</s>'
ScoreTuple = collections.namedtuple('ScoreTuple', ['MaxBLEU', 'MDS', 'PDS'])


def parse_response_file(filename, eos=None):
    """
    Parse a response file into a list of list of responses.

    :param filename:
    :param eos:
    :return:
    """
    if eos is None:
        eos = DEFAULT_EOS

    def split_responses(line):
        """
        Turn a line into a list of response.
        Each response is split into a list of tokens.

        :param line:
        :return:
        """
        responses = line.split(eos)
        return [response.strip().split() for response in responses]

    with open(filename) as f:
        lines = f.readlines()

    return list(map(split_responses, lines))


def run_all_metrics(response_file, eos=None):
    """
    Run the three metrics (MaxBLEU, MDS, PDS) on the response_file.
    Return the average of each of them.

    :param response_file:
    :param eos:
    :return:
    """
    _logger.info('loading response_file %s', response_file)
    response_sets = parse_response_file(response_file, eos)
    _logger.info('response sets in total: %d', len(response_sets))

    eval_dataset = _EvalDataset.create_from_pickle()
    response_reference_pairs = [(response, eval_dataset.get_reference_group(i)) for i, response in
                                enumerate(response_sets)]

    _logger.info('running MDS...')
    MDS = np.mean(_lsdscc_metrics.mean_diversity_score(hy, r) for hy, r in response_reference_pairs)

    _logger.info('running MDS...')
    PDS = np.mean(_lsdscc_metrics.probabilistic_diversity_score(hy, r) for hy, r in response_reference_pairs)

    _logger.info('running MDS...')
    maxBLEU = np.mean(_lsdscc_metrics.maxBLEU(hy, r) for hy, r in response_reference_pairs)
    return ScoreTuple(MaxBLEU=maxBLEU, MDS=MDS, PDS=PDS)
