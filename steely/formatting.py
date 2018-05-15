def _new_wrapper(prefix, suffix=None):
    return lambda text: _wrap(text, prefix, suffix)


def _wrap(text, prefix, suffix):
    if suffix == None:
        suffix = prefix
    return f'{prefix}{text}{suffix}'


bold = _new_wrapper('*')
italic = _new_wrapper('_')
monospace = _new_wrapper('`')
strikethrough = _new_wrapper('~')
latex = _new_wrapper('\\(', '\\)')
code_block = _new_wrapper('```\n', '\n```')
