#!/usr/bin/env python3

'''
.define [`code`] <command_name> <some text ...>
.define list

.define allows you to add commands which contains text.
They can be accessed via ~<command_name>, and will output what you put in.

.define code <text> will format the input as code.
'''


from tinydb import TinyDB, Query
from formatting import *


__author__ = 'alexkraak'
COMMAND = 'define'
CMD_DB = TinyDB('databases/quote.json')
CMD = Query()
LIMIT = 20
ANGRY_STRING = 'please use in form .define <command_name> <command text>'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if message == 'list':
        user_cmds = ', '.join((command['cmd'] for command in CMD_DB))
        bot.sendMessage(code_block(user_cmds),
                        thread_id=thread_id, thread_type=thread_type)
        return
    if not ' ' in message:
        bot.sendMessage(ANGRY_STRING, thread_id=thread_id,
                        thread_type=thread_type)
        return
    command, text = message.split(' ', 1)
    if command == 'code':
        if ' ' in text:
            command, text = text.split(' ', 1)
            text = code_block(text)
        else:
            bot.sendMessage(ANGRY_STRING, thread_id=thread_id,
                            thread_type=thread_type)
            return
    if not command.startswith('~'):
        command = f'~{command}'
    if len(command) > LIMIT:
        bot.sendMessage("that's too long dickhead",
                        thread_id=thread_id, thread_type=thread_type)
        return
    search = CMD_DB.get(CMD.cmd == command)
    if search == None:
        CMD_DB.insert({"cmd": command, "text": text})
        bot.sendMessage(f'Your command can be run with {command}',
                        thread_id=thread_id, thread_type=thread_type)
    else:
        CMD_DB.update({"text": text}, CMD.cmd == command)
        bot.sendMessage(f'Your command {command} has been updated',
                        thread_id=thread_id, thread_type=thread_type)
