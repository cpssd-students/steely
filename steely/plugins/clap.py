'''.mock mocks the previous command'''


import re


__author__ = 'sentriz'
COMMAND = '.clap'


def mock(string):
    return re.sub(r'(\w)\s(\w)', r'\1 👏 \2', string)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(mock(message.text), thread_id=thread_id, thread_type=thread_type)
