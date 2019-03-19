"""Handle dataset loading."""
import os
import json
import zipfile
import collections
import pickle

__all__ = ["EvalDataset"]

DATA_ROOT = os.path.join(os.path.dirname(__file__), 'data')
GROUP_FILE = os.path.join(DATA_ROOT, 'test.group.json')
GROUP_PICKLE_FILE = os.path.join(DATA_ROOT, 'eval_dataset.pkl')
DATASET_ZIP_FILE = os.path.join(DATA_ROOT, 'dataset.zip')
DATASET_TXT = 'dataset.txt'

_QUERY_RESPONSE_SEPARATOR = '<EOS>#TAB#'

_TRAIN_PERCENTAGE = 0.85


def _process_reference_group(group):
    """
    Process a reference_group from *raw* data loaded from json for use in Python.
    :param group: dict. key is id of a subgroup. value is a list of string as the references of a subgroup.
    :return: a list of subgroups (members). Each subgroup is a list of sentences.
    Each sentence is a list of tokens. Every sentence in the raw data is already tokenized so we can
    simply split it.
    """
    new_group = []
    for member in group.values():
        new_group.append([ref.split() for ref in member])
    return new_group


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
    with zipfile.ZipFile(DATASET_ZIP_FILE) as dataset_zip:
        with dataset_zip.open(DATASET_TXT) as f:
            raw_data = f.read().decode()
    return [line.split(_QUERY_RESPONSE_SEPARATOR) for line in raw_data.splitlines()]


def _split_dialogs(dialogs):
    """
    Split a list of dialogs into a training set (85%) and a validation set (15%).
    :param dialogs: a list of query-response pairs.
    :return: a 2-tuple. Sub list of the dialogs.
    """
    total = len(dialogs)
    for_train = round(total * _TRAIN_PERCENTAGE)
    return dialogs[:for_train - 1], dialogs[for_train:]


class EvalDataset(collections.namedtuple('EvalDataset', ['reference_groups', 'test_queries'])):
    """
    The dataset used for evaluation.

    Fields:
        reference_groups: A JSON dict of the human-annotated query-response groups.
        The key is a query. The value is a dict, whose key is the ID of a group and
        value is a list of responses of that group.

        test_queries: A list of queries, the keys of the reference_groups.
    """

    @classmethod
    def create(cls):
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
    def create_from_pickle(cls):
        """
        Create an EvalDataset instance by loading from a pickle file.
        :return:
        """
        with open(GROUP_PICKLE_FILE, 'rb') as f:
            obj = pickle.load(f)
        assert isinstance(obj, cls)
        return obj

    def get_reference_group(self, query):
        """
        Return the reference group for this query.
        :param query: Union[int, str] a string used as a key to the query-reference-group mapping.
        If it is an integer, the query string is first looked by calling `self.get_test_query_at()`.
        :return: a list of reference set. A reference set is a list of reference sentence.
        """
        if isinstance(query, int):
            query = self.get_test_query_at(query)
        return self.reference_groups[query]

    def __repr__(self):
        return object.__repr__(self)

    def get_test_query_at(self, index):
        return self.test_queries[index]
