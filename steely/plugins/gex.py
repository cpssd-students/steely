'''handle gex decks and associated sex'''

__author__ = 'iandioch'
COMMAND = '.gex'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage('No such gex command found\u203D', thread_id=thread_id, thread_type=thread_type)
