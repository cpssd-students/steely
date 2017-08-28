#!/usr/bin/env python3

'''
.define [`code`] <command_name> <some text ...>
.define list

.define allows you to add commands which contains text.
They can be accessed via ~<command_name>, and will output what you put in.

.define code <text> will format the input as code.
'''


from tinydb import TinyDB, Query


__author__ = 'sentriz'
COMMAND = '.stats'
CMD_DB = TinyDB('stats.json')
CMD = Query()


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(str(CMD_DB.all()), thread_id=thread_id, thread_type=thread_type)
