#!/usr/bin/env python3

'''hello'''
import random


__author__ = 'sentriz'
COMMAND = 'drunk'


def shuffle(string):
    return ''.join(random.sample(string, len(string)))


def shuffle_middle(string):
    if len(string) <= 3:
        return string
    return string[0] + shuffle(string[1:-1]) + string[-1]


def shuffle_sentance(string):
    return " ".join(map(shuffle_middle, string.split()))


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(shuffle_sentance(message.text), thread_id=thread_id, thread_type=thread_type)


if __name__ == "__main__":
    print(shuffle_middle("hello"))
