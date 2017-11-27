#!/usr/bin/env python3

"""
gimme a number and see what happens
"""


import random


__author__ = 'devoxel'
COMMAND = None
STRINGS = ["NUMBERWANG!",
           "Another one",
           "Thaaaaaat's Numberwang!",
           "Okay", "Uh huh",
           "WangerNumb ;)"]
WEIGHTS = [3, 20, 2, 20, 20, 1]


def numberwang():
    return random.choices(STRINGS, weights=WEIGHTS)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    try:
        float(message)
    except ValueError:
        return
    bot.sendMessage(numberwang(), thread_id=thread_id, thread_type=thread_type)
