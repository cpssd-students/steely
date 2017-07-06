#!/usr/bin/env python3

from tinydb import TinyDB, Query

COMMAND = '.define'
CMD_DB = TinyDB('quote.json')
CMD = Query()

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message_split = message.split()
    search = CMD_DB.get(CMD.cmd == '~' + message_split[0])
    if len(message_split) >= 2:
        if search == None:
            CMD_DB.insert({"cmd": '~' + message_split[0],
                           "text": " ".join(message_split[1:])})
            bot.sendMessage('Your command can be run with ~' + message_split[0],
                            thread_id=thread_id, thread_type=thread_type)
            return
        else:
            CMD_DB.update({"text": " ".join(message_split[1:])}, CMD.cmd == '~' + message_split[0])
            bot.sendMessage('Your command ~{} has been updated'.format(message_split[0]),
                            thread_id=thread_id, thread_type=thread_type)
            return

    else:
        bot.sendMessage('please use in form .define <command_name> <command text>',
                        thread_id=thread_id, thread_type=thread_type)
        return

