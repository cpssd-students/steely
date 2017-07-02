import random

COMMAND = '.ht'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    heads = "http://random-ize.com/coin-flip/us-quarter/us-quarter-front.jpg"
    tails = "http://random-ize.com/coin-flip/us-quarter/us-quarter-back.jpg"
    bot.sendRemoteImage(heads if random.randint(0,1) == 0 else tails,
                        message=None,
                        thread_id=thread_id,
                        thread_type=thread_type)
