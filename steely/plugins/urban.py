'''
.ud <query>

find out what that slang means via. urban dictionary.

eg: .ud the kentucky klondike bar
'''

from urllib.parse import quote
import requests


__author__ = 'EdwardDowling'
COMMAND = 'ud'


def define(term):
    results = []
    term = quote(term)
    response = requests.get(
        'http://api.urbandictionary.com/v0/define?term=' + term)
    for result in response.json()['list']:
        return '{}\n "{}"'.format(result['definition'],
                                  result['example'])
    return ""


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    definition = define(message)
    if not message or not definition:
        bot.sendMessage('no results', thread_id=thread_id,
                        thread_type=thread_type)
        return
    bot.sendMessage(definition, thread_id=thread_id, thread_type=thread_type)
