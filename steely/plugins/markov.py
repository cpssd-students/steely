#!/usr/bin/env python3


import os
import random
import markovify
import time


__author__ = 'sentriz'
COMMAND = None
LOGFOLDER = 'logs'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not any(word in message.lower() for word in ('steely', 'reed', 'bot')):
        return
    if random.random() > 0.3:
        return
    log_path = os.path.join(LOGFOLDER, thread_type.name, thread_id)
    with open(log_path, 'r') as file:
        log_model = markovify.NewlineText(file.read())
        new_sentence = log_model.make_sentence(tries=100)
    if new_sentence:
        bot.sendMessage(new_sentence, thread_id=thread_id, thread_type=thread_type)
