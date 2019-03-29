# LSDSCC
LSDSCC stands for *Large Scale Domain Specific Conversion Corpus*, a dataset 
for dialogue generation proposed by Zhen Xu et al. in 2016.
Along with the dataset, they propose a set of diversity-oriented metrics to be used together with the dataset.
Since our primary interest is the *metrics*, we will focus on the proposed three metrics.

These metrics are: `MaxBLEU`, `Mean Diversity Score, MDS` and `Probabilistic Diversity Score, PDS`.
To use the metrics, models are supposed to generate multiple hypotheses in terms of a *query*.
The hypotheses are also call a *hypothesis set* to distinguish them from the single-hypothesis setting from the
other metrics. The metrics then use a *reference set* to evaluate the hypothesis set.
A reference set is all the ground truth responses to the query that are semantically acceptable.
For example, given the query

    Where is Mike?
    
The responses
- The kitchen. 
- Went to the cinema.
- Somewhere.
- I don't know.
- God know!

are all acceptable. The references are then divided into groups according to peer-wise semantic similarity
using human labeling. Using the above example, a possible division is:
- Group-1
    * The kitchen.
    * Went to cinema.
- Group-2
    * Somewhere.
- Group-3
    * I don't know.
    * God know!

Then each hypothesis `h_i` in the set is assigned to a group `k` by calculating the following formula:

    k = argmax_j Multi-BLEU(h_i, r_j)
    
where `r_j` is one of the group in the reference groups, `h_i` is a hypothesis in the hypothesis set
and `Multi-BLEU` evaluates the similarity between the hypothesis sentence and the reference sentences.
According to the paper, `Multi-BLEU` is the one used in (Madnani et al., 2008), but our implementation
parametrize this function as an `Aligner` and let you choose the proper one to satisfy your own need.

PDS and MDS are computed with a simple algorithm, shown in pseudo python code:

    def diversity_metrics(H: hypothesis_set, R: reference_set):
        for r_i in R:
            p_i = 1 / |R|
            pp_i = |r_i| / |R|
        
        for h_i in H:
            k = argmax(Multi_BLEU(h_i, R)
            MDS[k] = p_k
            PDS[k] = pp_k
            
        return sum(MDS for all k), sum(PDS for all k)
        
where `|R|` denotes the size of `R` and the `sum` in the last line sums over all `k`.
MaxBLEU is computed as the mean of `max(Multi_BLEU(h_i, R))` for all `h_i` in the hypothesis set.

# Document
## Core Data Structures
We build our API upon a few core data structures, namely the `HypothesisSet` and `ReferenceSet`.
However, thank to duck typing, you can use object of *any* type as input, as long as they have proper shapes.

A HypothesisSet is set of hypotheses to be evaluated by the metrics. Its shape is `(None, None, None)` and it is
a string tensor with exactly 3 dimensions. To create a HypothesisSet you can just write a python list with the right shape
or wrap it with the `HypothesisSet` constructor. Or you can load a list of `HypothesisSet` from a file with a predefined format.
The format is one hypothesis set on one line and each hypothesis of a set is separated by a `eos` token.
For example:

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

A ReferenceSet is the labelled reference set which has a hierarchical structure. Its shape is `(None, None, None, None)`
and it is a string tensor with exactly 4 dimensions. Like `HypothesisSet`, you can use plain python list as a ReferenceSet
or wrap it in a ReferenceSet. It also provide a classmethod to create one from a json dictionary (which is a python dict
resulted from a json format). You can also load a list of ReferenceSet from a json corpus using
`ReferenceSet.load_json_corpus()`.
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
With these two data structures you can pass them to the metrics functions and get the scores.

## The Metric Functions
Two variants of the metric are provided.

    # operates on a single hypothesis set.
    compute_score_on_hypothesis_set(hypothesis_set, reference_set, aligner=None)
    
    # operates on a corpus of hypothesis sets by taking average of each score.
    compute_score_on_corpus(hypothesis_corpus, reference_corpus, aligner=None)
    
The return value of both functions is a `namedtuple` with three fields (in that order): `mds, pds, max_bleu`,
holding values for the three metrics respectively.

## Aligner
The algorithm of the LSDSCC metrics uses `argmax()` to find the reference group that is the most similar to a
hypothesis semantically. An Aligner object is used to score the similarity between each reference group w.r.t a hypothesis.
The higher the Aligner's output is, the more similar the reference group and the hypothesis are.
NB: different Aligner may judge the degree of similarity different and thus affects the value of PDS and MDS.
Three Aligners and provided in `lsdscc.align` module.

# Install
Install from local folder is supported.
```bash
git clone https://github.com/neural-dialogue-metrics/LSDSCC.git
cd LSDSCC/
pip install -e .
```

# Dependencies
- nltk==3.4
- numpy>=numpy

# References
[1] LSDSCC: a Large Scale Domain-Specific Conversational Corpus for Response Generation with Diversity Oriented Evaluation Metrics. Zhen Xu et al. (2016)

[2] Are Multiple Reference Translations Necessary? Investigating the Value of Paraphrased Reference Translations in Parameter Optimization. Nitin Madnani et al. (2008)
