"""
It is Wednesday, my dudes
"""

__author__ = ('Smurphicus')
COMMAND = 'wednesday'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    wednesday_message = message.text + ", my dudes"
    bot.sendMessage(wednesday_message, thread_id=thread_id, thread_type=thread_type)
