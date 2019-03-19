from setuptools import setup

setup(
    name='lsdscc',
    version='0.1',
    description='Python implementation of the three metrics provide by LSDSCC',
    url='https://github.com/neural-dialogue-metrics/LSDSCC.git',
    author='cgsdfc',
    author_email='cgsdfc@126.com',
    keywords=[
        'NL', 'CL', 'MT',
        'natural language processing',
        'computational linguistics',
        'machine translation',
    ],
    packages=['lsdscc'],
    package_data={
        'lsdscc': ['data/*']
    },
    scripts=[],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache-v2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
    ],
    license='LICENCE.txt',
    long_description=open('README.md').read(),
    install_requires=[],
)
