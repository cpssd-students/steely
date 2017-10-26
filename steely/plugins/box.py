'''
.box <text>

.box will generate a cool lookin 3d box using the text.
the text must be between 6 and 19 characters.
'''

import random
from formatting import *


__author__ = 'sentriz'
COMMAND = 'box'


DIAGONAL = '/'
GAP = ' '


def gen_box(word):
    yield GAP*6 + GAP.join(word)
    yield GAP*4 + DIAGONAL + GAP + word[1] + GAP*(2*len(word)-5) + DIAGONAL + GAP + word[-2]
    yield GAP*2 + DIAGONAL + GAP*3 + word[2] + GAP*(2*len(word)-7) + DIAGONAL + GAP*3 + word[-3]
    yield GAP.join(word) + GAP*5 + word[-4]
    for n in range(len(word) - 5):
        yield word[n + 1] + GAP*5 + word[n+4] + GAP*(2*len(word) - 9) + word[-n-2] + GAP*5 + word[-n+len(word)-5]
    yield word[-4] + GAP*5 + GAP.join(word[::-1])
    yield word[-3] + GAP*3 + DIAGONAL + GAP*(2*len(word)-7) + word[2] + GAP*3 + DIAGONAL
    yield word[-2] + GAP + DIAGONAL + GAP*(2*len(word)-5) + word[1] + GAP + DIAGONAL
    yield GAP.join(word[::-1])


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage('word please', thread_id=thread_id, thread_type=thread_type)
    elif 5 < len(message) < 20:
        box = '\n'.join(gen_box(message))
        bot.sendMessage(code_block(box), thread_id=thread_id, thread_type=thread_type)
    else:
        bot.sendMessage("can't use \"{}\"".format(message), thread_id=thread_id, thread_type=thread_type)
