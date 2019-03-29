import json
import logging

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
        self._hypothesis_sentences = hypothesis_sentences
        pass

    def __iter__(self):
        return iter(self._hypothesis_sentences)

    def __len__(self):
        """
        Return the number of hypotheses in the set.

        :return:
        """
        return len(self._hypothesis_sentences)

    def __getitem__(self, item):
        return self._hypothesis_sentences[item]

    def __str__(self):
        return "\n".join("%d: %r" % (i, h) for i, h in enumerate(self._hypothesis_sentences))

    def __repr__(self):
        return '<%s with %d sentences>' % (self.__class__.__name__, len(self))

    @classmethod
    def from_line(cls, line, eos=None):
        if eos is None:
            eos = DEFAULT_EOS
        hypothesis = line.split(eos)
        return cls(
            [sentence.strip().split() for sentence in hypothesis]
        )

    @classmethod
    def load_corpus(cls, filename, eos=None):
        with open(filename) as f:
            return [cls.from_line(line, eos) for line in f.readlines()]


class ReferenceSet:
    """
    This class represents a 2-level multiple reference group.
    """

    def __init__(self, annotated_refs):
        self._reference_set = annotated_refs

    def __len__(self):
        return len(self._reference_set)

    def __iter__(self):
        return iter(self._reference_set)

    def __getitem__(self, item):
        return self._reference_set[item]

    @classmethod
    def from_json(cls, json_dict):
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

          :param json_dict: dict.
          :return: a nested list.
          """
        sorted_group = sorted(json_dict.items(), key=lambda kv: int(kv[0]))
        return cls([[ref.split() for ref in values] for _, values in sorted_group])

    @classmethod
    def load_json_corpus(cls, filename):
        with open(filename) as f:
            json_data = json.load(f)
        return [cls.from_json(json_dict) for _, json_dict in json_data.items()]
