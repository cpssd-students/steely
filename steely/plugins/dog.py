'''doggos sure are lovely'''


import requests


__author__ = 'itsdoddsy'
COMMAND = 'dog'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    json_response = response.json()
    bot.sendRemoteImage(json_response['message'],
                        thread_id=thread_id,
                        thread_type=thread_type)
