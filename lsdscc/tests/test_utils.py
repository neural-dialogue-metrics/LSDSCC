import unittest
from lsdscc.helper import make_ref_group
from lsdscc.helper import parse_response_line


class TestToRefGroup(unittest.TestCase):
    json_group = {
        '1': [
            'what you see is what you get',
            'what you see is what you mean',
        ],
        '2': [
            'free as freedom',
            'free as free beer',
        ]
    }
    ref_group = [
        [
            'what you see is what you get'.split(),
            'what you see is what you mean'.split(),
        ],
        [
            'free as freedom'.split(),
            'free as free beer'.split(),
        ]
    ]

    def test_example(self):
        self.assertEqual(
            first=self.ref_group,
            second=make_ref_group(self.json_group),
        )


class TestParseResponseLine(unittest.TestCase):

    def test_example(self):
        s1 = 'you can fool everyone for a time'
        s2 = 'and you can fool some people forever'
        s3 = 'but you can never fool everyone forever'
        # Note we use a different separator.
        line = r' <\s> '.join((s1, s2, s3))
        responses = [
            s1.split(),
            s2.split(),
            s3.split(),
        ]
        self.assertEqual(responses, parse_response_line(line, eos=r'<\s>'))
