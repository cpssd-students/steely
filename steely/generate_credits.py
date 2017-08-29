#!/usr/bin/env python3


import os
import imp
import fileinput
from operator import itemgetter
from utils import list_plugins


FILENAME = '../README.md'
IDENTIFIER = 'creditline'
START_IDENTIFIER = '---------------|'


def get_plugin_name(plugin):
    return plugin.__name__[:-3]


def get_plugin_author(plugin):
    author_s = plugin.__author__
    if is_multi_author(author_s):
        return ', '.join(map(markdown_link_of, author_s))
    return markdown_link_of(author_s)


def markdown_link_of(author):
    return f'[{author}](https://github.com/{author}/)'


def is_multi_author(authors):
    valid_types = (list, tuple)
    return any(isinstance(authors, type) for type in valid_types)


def get_credits():
    for plugin in list_plugins():
        yield get_plugin_name(plugin), \
              get_plugin_author(plugin)


def format_credit_line(name, author):
    return f'|{name}|{author}| {IDENTIFIER}'


def make_new_credits():
    credits = sorted_credits(get_credits())
    return '\n'.join(format_credit_line(name, author) \
                     for name, author in credits)


def sorted_credits(credits):
    ''' sort credits by author, then plugin name
    '''
    return sorted(credits, key=itemgetter(1, 0))


def change_credits():
    new_credits = make_new_credits()
    for line in fileinput.input(FILENAME, inplace=True):
        if line.rstrip().endswith(START_IDENTIFIER):
            print(f'{line}{new_credits}')
        elif line.rstrip().endswith(IDENTIFIER):
            continue
        else:
            print(line, end='')


if __name__ == '__main__':
    change_credits()
