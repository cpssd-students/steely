#!/usr/bin/env python3
'''sheriff'''


import random
import requests
import re


__author__ = 'sentriz'


def parse_emoji_data(url):
    raw_data = requests.get(url).json()
    return {info["char"]: name for name, info in raw_data.items()}


COMMAND = 'sheriff'
TEMPLATE = """⠀ ⠀ ⠀  🤠\n　   {emoji}{emoji}{emoji}\n    {emoji}   {emoji}　{emoji}\n   👇   {emoji}{emoji} 👇\n  　  {emoji}　{emoji}\n　   {emoji}　 {emoji}\n　   👢     👢\nhowdy. i'm the sheriff of {name}"""
EMOJI_URL = 'https://raw.githubusercontent.com/muan/emojilib/master/emojis.json'
EMOJI_DATA = parse_emoji_data(EMOJI_URL)


def get_emoji_name(emoji):
    name = EMOJI_DATA.get(emoji)
    if name: 
        return name.replace("_", " ")
    return emoji


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    message = re.sub(r'\s+', '', message)
    if not message or len(message) != 1:
        send_message("no")
        return
    name = get_emoji_name(message)
    send_message(TEMPLATE.format(emoji=message, name=name))
