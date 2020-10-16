#!/usr/bin/env python3


from tinydb import Query
from tinydb.operations import increment
from utils import new_database


__author__ = 'sentriz'
COMMAND = None
CMD_DB = new_database('stats')
CMD = Query()
TILDA_DB = new_database('quote')
TILDA = Query()
COMMAND_IDENTIFIERS = set(['.', '~', '/'])


def first_word_of(message):
    if ' ' in message:
        message = message.split()[0]
    return message


def is_tilda_command(command):
    return bool(TILDA_DB.search(TILDA.cmd == command))


def looks_like_command(command):
    return any(command.startswith(char) for char in COMMAND_IDENTIFIERS)


def is_command(command, plugins):
    if not looks_like_command(command):
        return False
    stripped_command = (command[1:] if command[0]
                        in COMMAND_IDENTIFIERS else command)
    if stripped_command in plugins:
        return True
    elif is_tilda_command(command):
        return True
    return False


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    command = first_word_of(message)
    plugins = bot.plugins
    if not is_command(command, plugins):
        return
    stat_search = CMD_DB.get(CMD.command == command)
    if not stat_search:
        CMD_DB.insert({'command': command, 'count': 1})
    else:
        CMD_DB.update(increment('count'), CMD.command == command)
