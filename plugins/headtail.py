
from random import randint


COMMAND = '.ht'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(random.choice(['http://random-ize.com/coin-flip/us-quarter/us-quarter-front.jpg',
                                   'http://random-ize.com/coin-flip/us-quarter/us-quarter-back.jpg']),
                    thread_id=thread_id, thread_type=thread_type)
