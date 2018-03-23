'''
hello sam
'''


__author__ = 'izaakf'
COMMAND = 'hello'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage('hello sam', thread_id=thread_id, thread_type=thread_type)
