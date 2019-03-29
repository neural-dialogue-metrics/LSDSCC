import pathlib

DATA_ROOT = pathlib.Path(__file__).parent
assert DATA_ROOT.is_dir()

QUERY_FILE = DATA_ROOT / 'query.txt'
RESPONSE_FILE = DATA_ROOT / 'response.txt'
GROUP_FILE = DATA_ROOT / 'groups.json'

N_HYPOTHESES = 8
N_REFERENCES = 8
N_REF_SETS = 4