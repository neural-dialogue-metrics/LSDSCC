import shutil
import os
import tempfile
import subprocess
import re
import logging

PERL_FILE = os.path.join(os.path.dirname(__file__), 'multi-bleu.pl')
TRANSLATION_NAME = 'trans.txt'
REFERENCE_SUFFIX = '_ref.txt'
_OUTPUT_PATTERN = re.compile(r'BLEU = (\d+\.\d+/?){4}')

_logger = logging.getLogger(os.path.basename(__file__))


def _parse_output(out):
    """
    >>> out = 'BLEU = 42.9/18.2/0.0/0.0 (BP=1.000, ratio=0.875, hyp_len=14, ref_len=16)'
    >>> _parse_output(out)
    [42.9, 18.2, 0.0, 0.0]

    :param out:
    :return:
    """
    out = out[len('BLEU = '):out.find('(') - 1]
    numbers = out.split('/')
    return list(map(float, numbers))


def compute_multi_bleu(translation, references, ignore_case=False):
    """
    Compute BLEU-1 to BLEU-4 using the moses multi-bleu.pl script.

    Reference file and system output have to be sentence-aligned (line X in the reference file corresponds to line X
    in the system output). If multiple reference translation exist, these have to be stored in separated files and
    named reference0, reference1, reference2, etc. All the texts need to be tokenized.

    :param translation: a sentence.
    :param references: a list of sentences.
    :param ignore_case: True if case is ignored.
    :return: a 4-tuple, BLEU from 1 to 4.
    """
    tmpdir = tempfile.mkdtemp()
    _logger.info('create_from_json tmpdir %s', tmpdir)

    trans_filename = os.path.join(tmpdir, TRANSLATION_NAME)
    with open(trans_filename, 'w') as f:
        f.write(' '.join(translation))

    _logger.info('write translation file %s', trans_filename)

    ref_file_list = []
    for i, ref in enumerate(references):
        ref_filename = os.path.join(tmpdir, '%d%s' % (i, REFERENCE_SUFFIX))
        ref_file_list.append(ref_filename)
        with open(ref_filename, 'w') as f:
            f.write(' '.join(ref))
        _logger.info('write %d reference file %s', i, ref_filename)

    if not os.path.exists(PERL_FILE):
        raise RuntimeError('perl script not exist')

    cmdline = [PERL_FILE]
    if ignore_case:
        cmdline.append('-lc')

    cmdline.extend(ref_file_list)
    _logger.info('invoke %s', ' '.join(cmdline))

    with open(trans_filename) as input_:
        output = subprocess.check_output(cmdline, stdin=input_)
    output = output.decode()
    _logger.info('output is %r', output)
    shutil.rmtree(tmpdir)
    _logger.info('remove tmpdir')
    return _parse_output(output)


if __name__ == '__main__':
    # Test compute_multi_bleu.
    logging.basicConfig(level=logging.INFO)

    ref1 = 'It is a guide to action that ensures that the military' \
           ' will forever heed Party commands .'
    ref2 = 'It is the guiding principle which guarantees ' \
           'the military forces always being under the command of the Party .'
    ref3 = 'It is the practical guide for the army always to heed the directions of the party .'

    trans = 'It is to insure the troops forever hearing the activity ' \
            'guidebook that party direct .'

    scores = compute_multi_bleu(trans, [ref1, ref2, ref3])
    print(scores)
