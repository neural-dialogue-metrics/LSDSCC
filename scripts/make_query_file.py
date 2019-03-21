"""
This script creates a query file from the test.group.json.
The query file should be used as a part of the benchmark data.
Specifically, the model takes the query file and generates responses for
each query and then those responses are passed to the evaluator to get the score.

The format of query file is one query sentence per line.
"""
import argparse
import json
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('test_group_file', help='test group file in json format')
    parser.add_argument('output', help='output file to write the list of queries')
    args = parser.parse_args()

    with open(args.test_group_file) as f:
        data = json.load(f)
    logging.info('read json file %s', f.name)

    with open(args.output, 'w') as f:
        f.writelines('%s\n' % line for line in data.keys())
    logging.info('write output file %s', f.name)
