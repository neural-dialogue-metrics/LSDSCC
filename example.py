from lsdscc.dataset import Dataset
from lsdscc.metrics import mean_diversity_score
from lsdscc.metrics import probabilistic_diversity_score

if __name__ == '__main__':
    dataset = Dataset.create()
    query = dataset.get_test_query_at(0)
    responses = [
        "believe in god , why not ?",
        "yes , there is",
        "I am not sure , either",
        "Just forget it",
    ]
    reference_group = dataset.get_reference_group(0)
    mds = mean_diversity_score(responses, reference_group)
    pds = probabilistic_diversity_score(responses, reference_group)

    print('Query: %s' % query)
    print('MDS: %f' % mds)
    print('PDS: %f' % pds)
