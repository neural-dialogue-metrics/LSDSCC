"""
The data structure module.
"""
import io
import json
import logging

from lsdscc.data import TEST_GROUP_JSON

_logger = logging.getLogger(__name__)
DEFAULT_EOS = '</s>'

__all__ = [
    "HypothesisSet",
    "ReferenceSet",
]


class HypothesisSet:
    """
    This a simple wrapper of a list of sentence representing the hypothesis set.
    This class makes the headache of thinking of deeply-nested list less killing.
    """

    def __init__(self, hypothesis_sentences):
        self._hypothesis_set = hypothesis_sentences
        pass

    def __iter__(self):
        return iter(self._hypothesis_set)

    def __len__(self):
        """
        Return the number of hypotheses in the set.

        :return:
        """
        return len(self._hypothesis_set)

    def __getitem__(self, item):
        return self._hypothesis_set[item]

    def __str__(self):
        return "\n".join("%d: %r" % (i, h) for i, h in enumerate(self._hypothesis_set))

    def __repr__(self):
        return '<%s with %d hypotheses>' % (self.__class__.__name__, len(self))

    @classmethod
    def from_line(cls, line, eos=None):
        """
        Create a HypothesisSet from a line of string.

        :param line:
        :param eos:
        :return:
        """
        if eos is None:
            eos = DEFAULT_EOS
        hypothesis = line.split(eos)
        return cls(
            [sentence.strip().split() for sentence in hypothesis]
        )

    @classmethod
    def load_corpus(cls, filename, eos=None):
        """
        Load a list of HypothesisSet from a plain text file.

        :param filename:
        :param eos:
        :return:
        """
        _logger.info('loading hypothesis corpus %s', filename)
        with open(filename) as f:
            return [cls.from_line(line, eos) for line in f.readlines()]


class ReferenceSet:
    """
    This class represents a 2-level multiple reference group.
    """

    def __init__(self, reference_set, query=None):
        self._reference_set = reference_set
        self._query = query

    def __len__(self):
        return len(self._reference_set)

    def __iter__(self):
        return iter(self._reference_set)

    def __getitem__(self, item):
        return self._reference_set[item]

    @property
    def n_references(self):
        """
        Return the total number of references.
        """
        return sum(len(refs) for refs in self._reference_set)

    @property
    def query(self):
        """
        Return the associated query (if any).
        """
        return self._query

    def __repr__(self):
        return '<%s with %d groups, %d references>' % (
            self.__class__.__name__, len(self), self.n_references
        )

    @classmethod
    def from_json(cls, json_dict, query=None):
        """
          Turn a json dict representing a reference group into the format used by us.
          A reference group has many subgroups, each of which is semantically independent to one another.
          A subgroup has many in-group sentences, each of which shares a similar semantic with one another.
          The structure of a reference group can be viewed as a superset of semantic clusters of references.

          The format of the json dict is:
              1. The key is a str -- the subgroup id.
              2. The value is a list of str -- the member references of a subgroup.

          Our format is:
              1. The dict is replaced by a list. The order of the items follows the keys of the json dict.
              2. Each sentence str is split into a list.

          :param query:
          :param json_dict: dict.
          :return: a nested list.
          """
        sorted_group = sorted(json_dict.items(), key=lambda kv: int(kv[0]))
        return cls(
            reference_set=[[ref.split() for ref in values] for _, values in sorted_group],
            query=query,
        )

    @classmethod
    def load_json_corpus(cls, filename=None):
        """
        Load a list of ReferenceSet from a json file.

        :param filename: the file in json format. default to load the builtin lsdscc
        test set.
        :return: List[ReferenceSet]
        """
        if filename is None:
            filename = TEST_GROUP_JSON
        _logger.info('loading reference corpus %s', filename)
        with open(filename) as f:
            json_data = json.load(f)
        return [cls.from_json(json_dict, query) for query, json_dict in json_data.items()]

    def __str__(self):
        with io.StringIO() as f:
            print('query: %s' % self._query, file=f)
            for i, refs in enumerate(self._reference_set):
                print('group-%d:' % i, file=f)
                for j, reference in enumerate(refs):
                    print('  %d: %r' % (j, reference), file=f)
            return f.getvalue()
