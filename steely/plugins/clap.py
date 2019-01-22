'''.clap claps 👏 the 👏 previous 👏 message'''


import re


__author__ = ('sentriz', 'devoxel')
COMMAND = 'clap'


def mock(string):
    return re.sub(r'(?<=\w)\s+(?=\w)', r' 👏 ', string)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(mock(message.text.strip()),
                    thread_id=thread_id, thread_type=thread_type)
