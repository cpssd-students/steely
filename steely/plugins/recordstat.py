#!/usr/bin/env python3


from tinydb import TinyDB, Query
from tinydb.operations import increment


__author__ = 'sentriz'
COMMAND = None
CMD_DB = TinyDB('stats.json')
CMD = Query()


def parsed(message):
    if ' ' in message:
        message = message.split()[0]
    return message


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message.startswith('.'):
        return
    command = parsed(message)
    if not command in bot.plugins:
        return
    search = CMD_DB.get(CMD.command == command)
    if not search:
        print(command, 'didnt exist')
        CMD_DB.insert({'command': command, 'count': 1})
        return
    else:
        print(command, 'did exist')
        CMD_DB.update(increment('count'), CMD.command == command)
