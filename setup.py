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

from setuptools import setup

from lsdscc import __version__

setup(
    name='lsdscc',
    version=__version__,
    description='Python implementation of the three metrics proposed by LSDSCC',
    url='https://github.com/neural-dialogue-metrics/LSDSCC.git',
    author='Cong Feng',
    author_email='cgsdfc@126.com',
    keywords=[
        'NL', 'CL', 'MT', 'NLG',
        'natural language processing',
        'computational linguistics',
        'machine translation',
        'natural language generation',
    ],
    packages=[
        'lsdscc',
        'lsdscc.tests',
    ],
    package_data={
        # The dataset.zip is not installed currently.
        'lsdscc': ['data/*.txt', 'data/*.json', 'data/*.py'],
        'lsdscc.tests': ['data/*'],
    },
    scripts=['bin/lsdscc_metrics.py'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
    ],
    license='LICENCE.txt',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'nltk'],
)
