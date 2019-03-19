from lsdscc.dataset import EvalDataset
import pickle
import logging
import argparse

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file', help='where to dump the pickled object')
    args = parser.parse_args()

    logging.info('loading dataset...')
    dataset = EvalDataset.create()

    with open(args.output_file, 'wb') as f:
        pickle.dump(dataset, f)
    logging.info('write to file %s', f.name)
