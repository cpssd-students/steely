'''gives the previous command ａｅｓｔｈｅｔｉｃ'''


import random


__author__ = 'iandioch'
COMMAND = '.shout'


def shout(message):
    parts = message.split('.')
    out = ''
    for part in parts:
        out += part.upper() + ''.join(random.choices(['!', '1'], weights=[5, 1], k=random.randint(2, 8)))
    return out


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(shout(message.text), thread_id=thread_id, thread_type=thread_type)
