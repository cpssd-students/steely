from steely.formatting import *
from nose.tools import assert_equal


def test_code_blocks():
    data = [
        ('foo',              '```\nfoo\n```'),
        ('bar',              '```\nbar\n```'),
        ('code\ngoes\nhere', '```\ncode\ngoes\nhere\n```'),
    ]
    for text, expected_text in data:
        yield assert_equal, expected_text, code_block(text)


def test_bold_text():
    data = [
        ('hey',       '*hey*'),
        ('bold boys', '*bold boys*'),
        ('\n\n\n', '*\n\n\n*'),
    ]
    for text, expected_text in data:
        yield assert_equal, expected_text, bold(text)


def test_italic_text():
    data = [
        ('foo',     '_foo_'),
        ('bar',     '_bar_'),
        ('b\na\nz', '_b\na\nz_'),
    ]
    for text, expected_text in data:
        yield assert_equal, expected_text, italic(text)


def test_monospace_text():
    data = [
        ('foo',     '`foo`'),
        ('bar',     '`bar`'),
        ('b\na\nz', '`b\na\nz`'),
]
    for text, expected_text in data:
        yield assert_equal, expected_text, monospace(text)


def test_strikethrough_text():
    data = [
        ('foo', '~foo~'),
        ('bar', '~bar~'),
        ('baz', '~baz~'),
    ]
    for text, expected_text in data:
        yield assert_equal, expected_text, strikethrough(text)
