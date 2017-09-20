#!/usr/bin/env python3


from tinydb import TinyDB, Query


__author__ = 'alexkraak'
COMMAND = None
CMD_DB = TinyDB('databases/quote.json')
CMD = Query()


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    search = CMD_DB.get(CMD.cmd == message)
    if search != None:
        bot.sendMessage(search['text'],
                        thread_id=thread_id, thread_type=thread_type)
