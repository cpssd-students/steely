import requests
from steelybot import config

COMMAND = '.joke'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    r = requests.get("https://icanhazdadjoke.com/", headers={'Accept': 'application/json'})
    bot.sendMessage(r.json()['joke'], thread_id=thread_id, thread_type=thread_type)
