#!/usr/bin/env python3
'''sheriff'''


import random
import requests


__author__ = 'sentriz'
COMMAND = 'sheriff'
TEMPLATE = """⠀ ⠀ ⠀  🤠\n　   {char}{char}{char}\n    {char}   {char}　{char}\n   👇   {char}{char} 👇\n  　  {char}　{char}\n　   {char}　 {char}\n　   👢     👢\nhowdy. i'm the sheriff of {name}"""
EMOJI_DATA = requests.get(
    'https://raw.githubusercontent.com/muan/emojilib/master/emojis.json').json()


def emoji_to_name(emoji):
    for name, info in EMOJI_DATA.items():
        if info["char"] == emoji:
            return name.replace("_", " ")


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    name = emoji_to_name(message)
    if not name:
        return
    bot.sendMessage(TEMPLATE.format(char=message, name=name),
                    thread_id=thread_id, thread_type=thread_type)
