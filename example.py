from lsdscc.dataset import EvalDataset
from lsdscc.metrics import mean_diversity_score
from lsdscc.metrics import probabilistic_diversity_score

if __name__ == '__main__':
    dataset = EvalDataset.create_from_json()
    query = dataset._get_test_query_at(0)
    responses = [
        "believe in god , why not ?".split(),
        "yes , there is".split(),
        "I am not sure , either".split(),
        "Just forget it".split(),
    ]
    reference_group = dataset.get_reference_group(0)
    mds = mean_diversity_score(responses, reference_group)
    pds = probabilistic_diversity_score(responses, reference_group)

    print('Query: %s' % query)
    print('MDS: %f' % mds)
    print('PDS: %f' % pds)
