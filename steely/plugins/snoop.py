#!/usr/bin/env python3
"""
Reimagine the last message as if it were said by Snoop Dogg himself.
"""

import requests
from bs4 import BeautifulSoup


__author__ = 'CianLR'
COMMAND = '.snoop'
GIZOOGLE_URL = 'http://gizoogle.net/textilizer.php'


def snoop(text):
    r = requests.post(GIZOOGLE_URL, data={'translatetext': text})
    html = r.text.replace('height:250px;"/>', 'height:250px;">')  # Don't ask
    soup = BeautifulSoup(html, 'html.parser')
    return soup.textarea.string.encode('utf-8')


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    prev_message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(snoop(prev_message.text),
                    thread_id=thread_id,
                    thread_type=thread_type)


if __name__ == '__main__':
    def wrap(text):
        print(text)
        print(snoop(text))
        print()

    wrap("Hello my friend")
    wrap("It was a cold halloween night on Friday the thirteenth")
    wrap("Python's dynamic typing allows developers a great deal of freedom")
