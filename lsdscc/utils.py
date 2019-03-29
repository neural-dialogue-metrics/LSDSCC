import collections
import logging

_logger = logging.getLogger(__name__)
DEFAULT_EOS = '</s>'


def _split_responses(line, eos=None):
    """
    Turn a line into a list of response.
    Each response is split into a list of tokens.

    :param line: str.
    :return: a list of sentences.
    """
    if eos is None:
        eos = DEFAULT_EOS
    responses = line.split(eos)
    return [response.strip().split() for response in responses]


def parse_response_line(line, eos=None):
    """
    Parse a single line to a response set.

    :param line:
    :param eos:
    :return:
    """
    return _split_responses(line, eos)


def parse_response_file(filename, eos=None):
    """
    Parse a response file into a list of response set.
    The format of the response file:
        1. one line for one response set.
        2. responses in a response set are separated by `eos`.

    Example of response file:

        This is response 1 of set 1 </s> This is response 2
        This is response 3 </s> This is response 4 </s> one more response
        A single response on its own line

    :param filename: the response file.
    :param eos: the *end-of-sentence* token used to separate responses situated in one line.
    :return: Nested list of sentences.
    """
    _logger.info('loading response_file %s', filename)

    with open(filename) as f:
        return [_split_responses(line, eos) for line in f.readlines()]


def make_ref_group(json_data):
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

    :param json_data: dict.
    :return: a nested list.
    """
    sorted_group = sorted(json_data.items(), key=lambda kv: int(kv[0]))
    return [[ref.split() for ref in values] for _, values in sorted_group]


def make_annotated_refs(json_data):
    """
    Turn a json dict representing an annotated references into the format used by us.

    The format of the json dict is:
        1. The key is a str -- the query.
        2. The value is a dict -- as described by the input of make_ref_group.

    Our format is:
        1. A list of 2-tuple.
        2. Each tuple is (query:str, list:make_ref_group())

    :param json_data:
    :return:
    """
    return [(query, make_ref_group(refs)) for query, refs in json_data.items()]


def _create_response_reference_pairs(dataset, response_file, query_file=None, eos=None):
    response = parse_response_file(response_file, eos)

    if query_file is None:
        # If no query_file, use the natural order of the response_file.
        return [(res, dataset[i]) for i, res in enumerate(response)]
    # The order of query_file is used.
    with open(query_file) as f:
        query = [line.strip().lower() for line in f.readlines()]
    assert len(query) == len(response)
    return [(res, dataset[q]) for res, q in zip(response, query)]
