"""Handle dataset loading."""
import os
import json
import zipfile
import collections
import pickle
import logging

__all__ = [
    "EvalDataset",
    "TrainDataset",
]

DATA_ROOT = os.path.join(os.path.dirname(__file__), 'data')
GROUP_FILE = os.path.join(DATA_ROOT, 'test.group.json')
GROUP_PICKLE_FILE = os.path.join(DATA_ROOT, 'eval_dataset.pkl')
DATASET_ZIP_FILE = os.path.join(DATA_ROOT, 'dataset.zip')
DATASET_PKL_FILE = os.path.join(DATA_ROOT, 'dataset.pkl')

_DATASET_TXT = 'dataset.txt'
_QUERY_RESPONSE_SEPARATOR = '<EOS>#TAB#'
_TRAIN_PERCENTAGE = 0.85

_logger = logging.getLogger(__name__)




def _load_reference_groups():
    """
    Load and process the human annotated query-response-groups from json format.
    The raw json data is turned into a format for the ease of pythonic use.
    :return: dict.
    """
    with open(GROUP_FILE) as f:
        raw_data = json.load(f)
    return {query: _process_reference_group(group) for query, group in raw_data.items()}


def _load_dialogs():
    """
    Load the dialog records from a zip file.
    :return:
    """
    _logger.info('loading dialogs from %s...', DATASET_ZIP_FILE)
    with zipfile.ZipFile(DATASET_ZIP_FILE) as dataset_zip:
        with dataset_zip.open(_DATASET_TXT) as f:
            raw_data = f.read().decode()

    def make_pair(line):
        """
        Split a line into a query-response pair. Each sentence is a list of strings.

        :param line:
        :return:
        """
        return [utterance.split() for utterance in line.split(_QUERY_RESPONSE_SEPARATOR)]

    return [make_pair(line) for line in raw_data.splitlines()]


def _split_dialogs(dialogs):
    """
    Split a list of dialogs into a training set (85%) and a validation set (15%).
    :param dialogs: a list of query-response pairs.
    :return: a 2-tuple. Sub list of the dialogs.
    """
    total = len(dialogs)
    for_train = round(total * _TRAIN_PERCENTAGE)
    return dialogs[:for_train - 1], dialogs[for_train:]


def _load_from_pickle(cls, file):
    """
    Helper to load an object of cls from a pickle file.
    :param cls:
    :param file:
    :return:
    """
    with open(file, 'rb') as f:
        obj = pickle.load(f)
    assert isinstance(obj, cls)
    return obj


class TrainDataset(collections.namedtuple('TrainDataset', ['training_corpus', 'validation_corpus'])):
    """
    The dataset for training and validation which is a split of the original data.

    Fields:
        training_corpus: 85% of the query-response pairs.
        validation_corpus: 15% of the query-response pairs.
    """

    @classmethod
    def create_from_zip(cls):
        all_dialogs = _load_dialogs()
        ins = cls(*_split_dialogs(all_dialogs))
        return ins

    @classmethod
    def create_from_pickle(cls): return _load_from_pickle(cls, DATASET_PKL_FILE)

    # Prevent large print-out.
    __repr__ = object.__repr__


class EvalDataset:
    """
    The dataset used for evaluation.

    Fields:
        reference_groups: A JSON dict of the human-annotated query-response groups.
        The key is a query. The value is a dict, whose key is the ID of a group and
        value is a list of responses of that group.

        test_queries: A list of queries, the keys of the reference_groups.
    """

    def __init__(self, reference_groups, test_queries):
        self.reference_groups = reference_groups
        self.test_queries = test_queries

    @classmethod
    def create_from_json(cls):
        """
        Create a new EvalDataset by constructing from a json file.
        It may takes some time.
        :return:
        """
        reference_groups = _load_reference_groups()
        return cls(
            reference_groups=reference_groups,
            test_queries=list(reference_groups.keys()),
        )

    @classmethod
    def create_from_pickle(cls): return _load_from_pickle(cls, GROUP_PICKLE_FILE)

    def get_reference_group(self, query):
        """
        Return the reference group for this query.
        :param query: Union[int, str] a string used as a key to the query-reference-group mapping.
        If it is an integer, the query string is first looked by calling `self._get_test_query_at()`.
        :return: a list of reference set. A reference set is a list of reference sentence.
        """
        if isinstance(query, int):
            query = self._get_test_query_at(query)
        return self.reference_groups[query]

    # Prevent large print-out.
    __repr__ = object.__repr__

    def _get_test_query_at(self, index):
        return self.test_queries[index]

    def __contains__(self, query):
        return self.reference_groups.__contains__(query)

    def __len__(self):
        return len(self.reference_groups)

    def __getitem__(self, item):
        return self.reference_groups.__getitem__(item)
