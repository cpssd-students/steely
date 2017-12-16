'''Dirty talk like you're in Dundalk'''

import random
import re
import string

__author__ = ('iandioch')
COMMAND = 'flirt'

PHRASES = [
    "rawr~, {s}{sep}",
    "{s}, big boy{sep}",
    "{s} xo",
    "{s} bb{sep}",
    "babe, {s}{sep}",
    "hey xxx {s}{sep}",
    "{s} xxx",
    "{s} xx",
    "{s} xoxo",
    "hot stuff, {s}{sep}",
    "{s} bbz{sep}",
    "{s} 8==)",
    "I'm horny. {s}{sep}",
    "Do you want to come over tonight..? {s}{sep}",
    "My parents aren't home, {s}{sep}",
    "{s} ;)",
]

def flirt(message):
    if len(message) <= 1:
        return ''
    for sep in '.!?':
        s, sepfound, after = message.partition(sep)
        if random.random() < 0.75:
          numspace = len(s) - len(s.lstrip())
          s = ' '*numspace + random.choice(PHRASES).format(s=s.lstrip(), sep=sepfound)
        else:
          s = s + sepfound
        return s + flirt(after)
    return message

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    sauce = flirt(message.text)
    bot.sendMessage(sauce, thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
    print(flirt('hey brandon do you have a minute'))
    print(flirt('I need to talk to you about our lord and saviour steely for a minute. Please brandon.'))
    print(flirt('Fine then'))
    print(flirt('Your API was shit anyway'))
