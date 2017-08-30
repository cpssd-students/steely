#!/usr/bin/env python3


import os
import random
import markovify


COMMAND = None
LOGFOLDER = 'logs'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if random.random() > 0.2: # do it 20% of the time
        return
    log_path = os.path.join(LOGFOLDER, thread_type.name, thread_id)
    with open(log_path, 'r') as file:
        log_model = markovify.NewlineText(file.read())
    for _ in range(10):
        new_sentance = log_model.make_sentence()
        if new_sentance:
            break
    bot.sendMessage(new_sentance, thread_id=thread_id, thread_type=thread_type)
