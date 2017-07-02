
from random import randint


COMMAND = '.ht'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(random.choice(['Heads', Tails']), thread_id=thread_id, thread_type=thread_type)
