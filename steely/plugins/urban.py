'''
.ud <query>

find out what that slang means via. urban dictionary.

eg: .ud the kentucky klondike bar
'''


import requests


__author__ = 'EdwardDowling'
COMMAND = 'ud'


def define(term):
    results = []
    term = '+'.join(term.split())
    response = requests.get(
        'http://api.urbandictionary.com/v0/define?term=' + term)
    if response.json()['result_type'] != 'exact':
        return results
    for result in response.json()['list']:
        results.append(
            {'definition': result['definition'], 'example': result['example']})
    return results


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    definitions = define(message)
    if not message or not definitions:
        bot.sendMessage('no results', thread_id=thread_id,
                        thread_type=thread_type)
        return
    text = '{definition}\n "{example}"'.format(**definitions[0])
    bot.sendMessage(text, thread_id=thread_id, thread_type=thread_type)
