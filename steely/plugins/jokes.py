'''yer the joke'''


import requests
from steely import config


__author__ = 'EdwardDowling'
COMMAND = '.joke'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    r = requests.get("https://icanhazdadjoke.com/", headers={'Accept': 'application/json'})
    bot.sendMessage(r.json()['joke'], thread_id=thread_id, thread_type=thread_type)
