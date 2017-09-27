'''message -> aeegmss'''

import random

__author__ = 'iandioch'
COMMAND = '.scramble'

def scramble(message):
    words = message.split()
    if len(words) == 0:
        return ""
    elif len(words) > 250:
        return "You can't zucc me"
    out = random.choice(words)
    words.remove(out)
    while len(words):
        word = random.choice(words)
        words.remove(word)
        out += ' ' + word
    return out

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(scramble(message.text), thread_id=thread_id, thread_type=thread_type)
