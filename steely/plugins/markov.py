#!/usr/bin/env python3
import os
import random
import markovify
import time


__author__ = 'sentriz'
COMMAND = None
LOGFOLDER = 'logs'
PROBABILITY = 0.03


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if should_reply():
        message = generate_reply(thread_id, thread_type)
        if message:
            bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)


def should_reply():
    return random.random() < PROBABILITY


def generate_reply(thread_id, thread_type):
    log_path = os.path.join(LOGFOLDER, thread_type.name, thread_id)
    with open(log_path, 'r') as file_:
        log_model = markovify.NewlineText(file_.read())
        new_sentence = log_model.make_sentence(tries=100)
    return new_sentence
