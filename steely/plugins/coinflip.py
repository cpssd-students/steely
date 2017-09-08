'''
Flip a coin with .coinflip

You'll either get heads or tails.
'''


import random


__author__ = ('alexkraak', 'byxor')
COMMAND = '.coinflip'


def flip_coin():
    return "Heads" if random.randint(0, 1) else "Tails"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    result = flip_coin()
    bot.sendMessage(result, thread_id=thread_id, thread_type=thread_type)

