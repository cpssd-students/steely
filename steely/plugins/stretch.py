'''gives the previous message sttrreeetttccchhhheeeeddddd'''


import random


__author__ = 'CianLR'
COMMAND = '.stretch'
STRETCH_FACTOR = 5


def stretch(message):
    if not message:
        return ""
    if len(message) > 300:
        return "Too long you spammy fuck"
    out = ""
    count = 1
    for c in message:
        if random.random() < (STRETCH_FACTOR / len(message)):
            count += 1
        out += c * count
    return out


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(stretch(message.text), thread_id=thread_id, thread_type=thread_type)
