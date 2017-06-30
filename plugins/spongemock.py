import random


COMMAND = '.mock'


def mock(string):
    return ''.join([(c.upper(), c.lower())[random.randint(0, 1)] for c in string])


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(mock(message.text), thread_id=thread_id, thread_type=thread_type)
