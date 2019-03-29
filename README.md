# LSDSCC
LSDSCC stands for *Large Scale Domain Specific Conversion Corpus*, a dataset 
for dialogue generation proposed by Zhen Xu et al. in 2016.
Along with the dataset, they propose a set of diversity-oriented metrics to be used together with the dataset.
Since our primary interest is the *metrics*, we will focus on the proposed three metrics
and only talk about the dataset for training and testing briefly.

These metrics are: `MaxBLEU`, `Mean Diversity Score, MDS` and `Probabilistic Diversity Score, PDS`.
To use the metrics, models are supposed to generate a multiple of hypotheses in terms of a *query*.
The hypotheses are also call a *hypothesis set* to distinguish them from the single-hypothesis setting from the
other metrics. The metrics then use a *reference set* to evaluate the hypothesis set.
A reference set is all the ground truth responses to the query that are semantically acceptable.
For example, given the query

    Where is Mike?
    
The responses
- The kitchen. 
- Went to cinema.
- Somewhere.
- I don't know.
- God know!

are all acceptable. The references are then divided into groups according to peer-wise semantic similarity
, using human labeling. Using the above example, a possible division is:
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

# Usage


# Dependencies


# References
[1] LSDSCC: a Large Scale Domain-Specific Conversational Corpus for Response Generation with Diversity Oriented Evaluation Metrics. Zhen Xu et al. (2016)

[2] Are Multiple Reference Translations Necessary? Investigating the Value of Paraphrased Reference Translations in Parameter Optimization. Nitin Madnani et al. (2008)
