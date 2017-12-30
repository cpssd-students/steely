'''doggos sure are lovely'''

import requests

__author__ = 'itsdoddsy'
COMMAND = 'dog'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    imagefromapi = requests.get("https://dog.ceo/api/breeds/image/random")
    imageurl = imagefromapi.json()
    bot.sendRemoteImage(imageurl['message'],
                        message=None,
                        thread_id=thread_id,
                        thread_type=thread_type)
