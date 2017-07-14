from random import randint


COMMAND = '.skrrt'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage('sk{}t'.format('r'*randint(1, 6))*randint(1, 3),
        thread_id=thread_id, thread_type=thread_type)
