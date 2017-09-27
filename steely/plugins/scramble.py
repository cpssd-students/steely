'''"hey add me on kik" -> "kik me add hey on"'''

import random


__author__ = 'iandioch'
COMMAND = '.scramble'


def scramble(message):
    split_message = message.split()
    if len(split_message) == 0:
        return ""
    elif len(split_message) > 250:
        return "You can't zucc me"
    random.shuffle(split_message)
    return " ".join(split_message)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(scramble(message.text), thread_id=thread_id, thread_type=thread_type)
