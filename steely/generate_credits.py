#!/usr/bin/env python3


import os
import imp
import fileinput
from utils import list_plugins


FILENAME = '../README.md'


def get_plugin_name(plugin):
    return plugin.__name__.rstrip('.py')


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


def get_authors():
    for plugin in list_plugins():
        yield get_plugin_name(plugin), \
              get_plugin_author(plugin)


def remove_credits():
    for line in fileinput.input(FILENAME, inplace=True):
        if 'async' in line:
            continue
        print(line, end='')

if __name__ == '__main__':
    # print(*get_authors(), sep='\n')
    remove_credits()
