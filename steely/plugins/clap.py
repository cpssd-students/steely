'''.mock mocks the previous command'''
import random


__author__ = 'sentriz'
COMMAND = '.clap'


def mock(string):
    return string.replace(' ', ' 👏 ')

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(mock(message.text), thread_id=thread_id, thread_type=thread_type)
