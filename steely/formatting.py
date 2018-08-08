import functools


def _wrapper(prefix, suffix=None):
    if suffix == None:
        suffix = prefix
    return functools.partial(_wrap, prefix, suffix)


_wrap = lambda prefix, suffix, text: f'{prefix}{text}{suffix}'


bold = _wrapper('*')
italic = _wrapper('_')
monospace = _wrapper('`')
strikethrough = _wrapper('~')
latex = _wrapper('\\(', '\\)')
code_block = _wrapper('```\n', '\n```')
