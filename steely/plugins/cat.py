'''cattos sure are lovely'''

import requests
import random


__author__ = 'itsdoddsy'
COMMAND = 'cat'
FORMAT = ("png", "jpg")


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    params = {
        "type": FORMAT.choice(FORMAT)
    }
    response = requests.get('http://thecatapi.com/api/images/get',
                            params=params)
    bot.sendRemoteImage(respose.url,
                        message=None,
                        thread_id=thread_id,
                        thread_type=thread_type)
