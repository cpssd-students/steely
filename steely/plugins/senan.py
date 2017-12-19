'''splooge'''

import random

__author__ = 'itsdoddsy'
COMMAND = 'senan'
SENAN = (
    "https://i.imgur.com/nGboTxZ.png",
	"https://i.imgur.com/3fQvF9r.png",
)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendRemoteImage(random.choice(SENAN),
                        message=None,
                        thread_id=thread_id,
                        thread_type=thread_type)