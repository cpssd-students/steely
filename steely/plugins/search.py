'''searches the previous message'''

import re

__author__ = 'EdwardDowling'
COMMAND = '.search'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    prev_message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1].text
    match = re.search(message, prev_message)
    if match:
        send_message('\n'.join([m for m in match]))
    else:
        send_message("no match idiot")
