"""Handle dataset loading."""
import os
import json
import zipfile
import collections

__all__ = ["Dataset"]

DATA_ROOT = os.path.join(os.path.dirname(__file__), 'data')
GROUP_FILE = os.path.join(DATA_ROOT, 'test.group.json')
DATASET_ZIP_FILE = os.path.join(DATA_ROOT, 'dataset.zip')
DATASET_TXT = 'dataset.txt'

_QUERY_RESPONSE_SEPARATOR = '<EOS>#TAB#'

_TRAIN_PERCENTAGE = 0.85


def _load_reference_groups():
    """
    Load the human annotated query-response-groups from json format.
    :return:
    """
    with open(GROUP_FILE) as f:
        return json.load(f)


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
    Split a list of dialogs into a training set (85%) and a test set (15%).
    :param dialogs: a list of query-response pairs.
    :return: a 2-tuple. Sub list of the dialogs. training_set, test_set.
    """
    total = len(dialogs)
    for_train = round(total * _TRAIN_PERCENTAGE)
    return dialogs[:for_train - 1], dialogs[for_train:]


class Dataset(collections.namedtuple('Dataset', ['dialogs',
                                                 'training_dialogs',
                                                 'test_dialogs',
                                                 'reference_groups',
                                                 'test_queries'])):
    """
    A simple interface to the loaded dataset.

    Fields:
        dialogs: A list of query-response pairs. This contains all the pairs loaded from the original dataset.txt.

        training_dialogs: First 85% of the dialogs for training.

        test_dialogs: The remaining pairs of dialogs for validating/testing.

        reference_groups: A JSON dict of the human-annotated query-response groups.
        The key is a query. The value is a dict, whose key is the ID of a group and
        value is a list of responses of that group.

        test_queries: A list of queries, the keys of the reference_groups.
    """

    @classmethod
    def create(cls):
        """
        Create a new Dataset by loading disk files.
        It may takes some time.
        :return: A new Dataset.
        """
        dialogs = _load_dialogs()
        train_dialogs, test_dialogs = _split_dialogs(dialogs)
        reference_groups = _load_reference_groups()

        return cls(
            dialogs=dialogs,
            training_dialogs=train_dialogs,
            test_dialogs=test_dialogs,
            reference_groups=reference_groups,
            test_queries=list(reference_groups.keys()),
        )

    def get_reference_group(self, query):
        """
        Return the reference group for this query.
        :param query: Union[int, str] a string used as a key to the query-reference-group mapping.
        If it is an integer, the query string is first looked by calling `self.get_test_query_at()`.
        :return: a list of reference set. A reference set is a list of reference sentence.
        """
        if isinstance(query, int):
            query = self.get_test_query_at(query)
        return self.reference_groups[query].values()

    def __repr__(self):
        return object.__repr__(self)

    def get_test_query_at(self, index):
        return self.test_queries[index]
