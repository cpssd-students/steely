#!/usr/bin/env python3


import os
import random
import markovify
import time


COMMAND = None
LOGFOLDER = 'logs'
CHANCE_OF_SEND = 0.1
DELAY = 120


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if random.random() > CHANCE_OF_SEND:
        return
    time.sleep(DELAY)
    log_path = os.path.join(LOGFOLDER, thread_type.name, thread_id)
    with open(log_path, 'r') as file:
        log_model = markovify.NewlineText(file.read())
        new_sentence = log_model.make_sentence(tries=100)
    if new_sentence:
        bot.sendMessage(new_sentence, thread_id=thread_id, thread_type=thread_type)
