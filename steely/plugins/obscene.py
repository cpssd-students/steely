#!/usr/bin/env python3
"""
Detects when people say naughty things and punishes them with a badge.
"""

import requests
from string import punctuation

from plugins import gex

__author__ = 'CianLR'
COMMAND = None
BAD_WORDS_URL = ('https://raw.githubusercontent.com/LDNOOBW/'
                 'List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/'
                 'master/en')
BAD_WORDS = set(requests.get(BAD_WORDS_URL).text.split('\n'))

CIAN_ID = '1845973042'
CARD_NAME = "obscene"
CARD_DESC = "WARNING: This person is not fit for a christian minecraft server"
CARD_IMAGE = "https://pics.me.me/this-a-christian-page-swearing-21946873.png"
card_made = CARD_NAME in gex.gex_codex()


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    global card_made
    if not card_made:
        gex.gex_create(CARD_NAME, [bot.uid, CIAN_ID], CARD_DESC)
        gex.gex_set_image(bot.uid, CARD_NAME, CARD_IMAGE)
        card_made = True

    message_words = {w.lower().strip(punctuation) for w in message.split()}
    if message_words & BAD_WORDS:
        gex.gex_give(bot.uid, CARD_NAME, author_id)
        return True
    return False


if __name__ == '__main__':
    def wrap(message):
        print(message, end=': ')
        print(main(None, None, message, None, None))

    wrap("What's up you meme loving fuck")
    wrap("I love tea")
    wrap("Shit, I love tea")
