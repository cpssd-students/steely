'''for those indecisive moments'''

__author__ = 'itsdoddsy'
COMMAND = 'choose'

import re
import random

ERRORS = ['fucking moron',
          'how about no',
          'pikachu', ]


def main(bot, author_id, message, thread_id, thread_type, *args, **kwargs):
    try:
        args = re.findall(r"\w+\b(?<!\bchoose)", message)
        bot.sendMessage(random.choice(args),
                        thread_id=thread_id, thread_type=thread_type)
    except IndexError:
        bot.sendMessage(random.choice(ERRORS),
                        thread_id=thread_id, thread_type=thread_type)
