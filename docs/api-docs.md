## Core Data Structures

We build our API upon a few core data structures, namely the `HypothesisSet` and `ReferenceSet`. However, thank to duck typing, you can use object of *any* type as input, as long as they have proper shapes.

A HypothesisSet is a set of hypotheses to be evaluated by the metrics. Its shape is `(None, None, None)` and it is a string tensor with exactly 3 dimensions. To create a HypothesisSet you can just write a python list with the right shape or wrap it with the `HypothesisSet` constructor. Or you can load a list of `HypothesisSet` from a file with a predefined format. The format is one hypothesis set on one line and each hypothesis of a set is separated by an `eos` token. For example:

    This </s> is </s> line 1 </s> with 4 hypothesis
    This </s> is </s> line 2 </s> with 4 hypothesis
    This </s> is </s> line 3 </s> with 4 hypothesis
    
```python
# Plain list as HypothesisSet
hypothesis_set = [
    'if a thing quakes like a duck'.split(),
    'and it walks like a duck'.split(),
    'and it swims like a duck'.split(),
    'then it must be a duck'.split()
]

from lsdscc import HypothesisSet

# You can directly wrap it and gain some convenient methods.
hypothesis_set = HypothesisSet(hypothesis_set)
print(hypothesis_set)

# Create from a line.
hypothesis_set = HypothesisSet.from_line('1;2;3', eos=';')

# Create from a file.
hypothesis_corpus = HypothesisSet.load_corpus('some/file')
```

A `ReferenceSet` is a labeled reference set that has a hierarchical structure. Its shape is `(None, None, None, None)` and it is a string tensor with exactly 4 dimensions. Like `HypothesisSet`, you can use a plain python list as a ReferenceSet or wrap it in a ReferenceSet. It also provides a `classmethod` to create one from a JSON dictionary (which is a python `dict` from a JSON format). You can also load a list of `ReferenceSet` from a json corpus using `ReferenceSet.load_json_corpus()`.

```python
reference_set = [
    ['A man can never have too many ties'.split()],
    ['And a woman can never have too many shoes'.split()],
    ['tik tok on the clock , but the party won \' t stop'.split()],
]

from lsdscc import ReferenceSet

# You can directly wrap it and gain some convenient methods.
reference_set = ReferenceSet(reference_set)
print(reference_set.n_references)

reference_corpus = ReferenceSet.load_json_corpus('some/json/file')

``` 
With these two data structures, you can pass them to the metrics functions and get the scores.

## Metric Functions

Two variants of the metric are provided.

    # operates on a single hypothesis set.
    compute_score_on_hypothesis_set(hypothesis_set, reference_set, aligner=None)
    
    # operates on a corpus of hypothesis sets by taking an average of each score.
    compute_score_on_corpus(hypothesis_corpus, reference_corpus, aligner=None)
    
The return value of both functions is a `namedtuple` with three fields (in that order): `mds, pds, max_bleu`, holding values for the three metrics respectively.

## Aligners

The algorithm of the LSDSCC metrics uses `argmax()` to find the reference group that is the most similar to a hypothesis semantically. An Aligner object is used to score the similarity between each reference group w.r.t a hypothesis. The higher the Aligner's output is, the more similar the reference group and the hypothesis are. NB: different Aligner may judge the degree of similarity differently and thus affects the value of PDS and MDS. Three Aligners and provided in `lsdscc.align` module.
