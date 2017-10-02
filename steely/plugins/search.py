'''.mock mocks the previous command'''

import re

__author__ = 'EdwardDowling'
COMMAND = '.search'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    prev_message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(string(re.search(message, prev_message)), thread_id=thread_id, thread_type=thread_type)
