import requests


COMMAND = '.joke'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    r = requests.get('http://webknox.com/api/jokes/oneLiner?apiKey=bejjacgahiubszovjbsszofuegekaws')
    bot.sendMessage(r.json()['text'], thread_id=thread_id, thread_type=thread_type)
