import unittest
from steely.plugins.url_expander import expand


class UrlExpansionTest(unittest.TestCase):

    def test_url_expansion(self):
        url_pairs = [
            ('https://tinyurl.com/2tx', 'google.com'),
            ('https://goo.gl/JLGDfs', 'facebook.com'),
            ('http://bit.ly/1cd2u0N', 'sourmath.com'),
        ]
        for short_url, expected_substring in url_pairs:
            expanded_url = expand(short_url)
            self.assertIn(expected_substring, expanded_url)


if __name__ == '__main__':
    unittest.main()

