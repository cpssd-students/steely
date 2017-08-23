from nose.tools import *
from steely.plugins.url import expand


def test_url_expansion():
    url_pairs = (
        ('https://tinyurl.com/2tx', 'google.com'),
        ('https://goo.gl/JLGDfs', 'facebook.com'),
        ('http://bit.ly/1cd2u0N', 'sourmath.com'),
    )
    for short_url, expected_substring in url_pairs:
        expanded_url = expand(short_url)
        yield assert_in, expected_substring, expanded_url
