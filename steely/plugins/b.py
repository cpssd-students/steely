from formatting import *

__author__ = 'byxor'
COMMAND = '.b'


REPLACEABLE = 'PpBbGg'
REPLACEMENT = '🅱️'


def encode(string):
    for sequence in REPLACEABLE:
        string = string.replace(sequence, REPLACEMENT)
    return string


def help():
    return code_block(f"{COMMAND} {encode('will transform the previous message into something a bit more exciting.')}",)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    last_message = lambda: bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1].text
    send = lambda message: bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    send(encode(last_message()))


__doc__ = help()
