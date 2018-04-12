'''searches the previous message'''

import re

__author__ = 'EdwardDowling'
COMMAND = 'search'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    prev_message = bot.fetchThreadMessages(
        thread_id=thread_id, limit=2)[1].text
    match = re.findall(message, prev_message)[:10]
    if match:
        send_message("\n".join(match))
    else:
        send_message("no match idiot")
