#!/usr/bin/env python3

from tinydb import TinyDB, Query

COMMAND = None
CMD_DB = TinyDB('../quote.json')
CMD = Query()

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    search = CMD_DB.search(CMD.cmd == message)
    if len(search) != 0:
        bot.sendMessage(search[0]['text'],
                        thread_id=thread_id, thread_type=thread_type)


