bold = lambda text: _wrap(text, '*')
italic = lambda text: _wrap(text, '_')
monospace = lambda text: _wrap(text, '`')
strikethrough = lambda text: _wrap(text, '~')


def code_block(text):
    TAG = '```'
    NEW_LINE = '\n'
    return _wrap(text, f'{TAG}{NEW_LINE}', f'{NEW_LINE}{TAG}')


def _wrap(text, prefix, suffix=None):
    if suffix == None:
        suffix = prefix
    return f'{prefix}{text}{suffix}'
