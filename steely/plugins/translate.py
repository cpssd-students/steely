'''
Translate the last message to another language

You must provide a standard language code as the argument.
E.g.

 > I hate sam

     .translate fr <

 > Je déteste sam

You can also translate multiple rounds by doing ".translate fr ga en"

The list of supported languages (and codes) are here:
https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/
'''

import requests

from paths import CONFIG

__author__ = 'CianLR'
COMMAND = 'translate'

# Key can be obtained from https://translate.yandex.com/developers/keys
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate(langs, text):
    if not langs:
        return "No language provided"
    for lang in langs:
        data = {
            'text': text,
            'lang': lang,
            'format': 'text',
            'key': CONFIG.TRANSLATE_API_KEY,
        }
        response = requests.post(URL, data=data).json()
        if response['code'] != 200:
            return response['message']
        text = response['text'][0]
    return text


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    last_message = bot.fetchThreadMessages(
        thread_id=thread_id, limit=2)[1].text
    bot.sendMessage(translate(message.split(), last_message),
                    thread_id=thread_id,
                    thread_type=thread_type)

if __name__ == '__main__':
    test_args = [
        (['fr'], 'I hate sam'),
        (['ru'], 'Greetings comrade'),
        (['ga'], 'Quiet road milk girl'),
        (['ga', 'en'], 'Hello there friend'),
    ]
    for l, t in test_args:
        print(t)
        print(l)
        print(translate(l, t))
        print()
