import argparse
from lsdscc import run_all_metrics

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('response_file', help='file containing responses to be evaluate')
    parser.add_argument('--query_file', '-q', help='query_file specifies the alignment between queries and responses')
    parser.add_argument('--eos', '-e', help='end-of-sentence indicator to use in the response file')
    args = parser.parse_args()

    score = run_all_metrics(args.response_file, args.eos)
    print('MaxBLEU: %f' % score.MaxBLEU)
    print('MDS: %f' % score.MDS)
    print('PDS: %f' % score.PDS)
