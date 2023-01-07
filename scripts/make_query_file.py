# MIT License
# 
# Copyright (c) 2019 Cong Feng.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
