from setuptools import setup

__version__ = '0.3.1'

setup(
    name='lsdscc',
    version=__version__,
    description='Python implementation of the three metrics proposed by LSDSCC',
    url='https://github.com/neural-dialogue-metrics/LSDSCC.git',
    author='cgsdfc',
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
