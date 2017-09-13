__author__ = 'izaakf'

COMMAND = '.hello'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage('Hello Sam', thread_id=thread_id, thread_type=thread_type)
