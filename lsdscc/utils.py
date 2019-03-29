import lsdscc.ds as _ds
import lsdscc.metrics as _metrics
import lsdscc.data as _data


def load_builtin_json_corpus():
    return _ds.ReferenceSet.load_json_corpus(_data.TEST_GROUP_JSON)


def compute_score_on_files(hypothesis_file, reference_file, eos=None, aligner=None):
    hypothesis_corpus = _ds.HypothesisSet.load_corpus(hypothesis_file, eos)
    reference_corpus = _ds.ReferenceSet.load_json_corpus(reference_file)
    return _metrics.compute_score_on_corpus(hypothesis_corpus, reference_corpus, aligner)
