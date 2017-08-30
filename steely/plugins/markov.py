#!/usr/bin/env python3


import os


COMMAND = None
LOGFOLDER = 'logs'


def looks_like_command(message):
    identifiers = '.', '~'
    return any(message.startswith(char) for char in identifiers)


def make_empty_log(log_path):
    log_dir, log_name = os.path.split(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(log_path):
        open(log_path, 'a').close()


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if looks_like_command(message):
        return
    log_path = os.path.join(LOGFOLDER, thread_type.name, thread_id)
    make_empty_log(log_path)
    with open(log_path, 'a') as file:
        file.write(message + '\n')
