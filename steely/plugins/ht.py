import random


COMMAND = '.ht'
HEADS_IMG = "http://random-ize.com/coin-flip/us-quarter/us-quarter-front.jpg"
TAILS_IMG = "http://random-ize.com/coin-flip/us-quarter/us-quarter-back.jpg"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendRemoteImage(HEADS_IMG if random.randint(0, 1) else TAILS_IMG,
                        message=None,
                        thread_id=thread_id,
                        thread_type=thread_type)
