#!/usr/bin/env python3


from tinydb import Query
from utils import new_database

__author__ = 'alexkraak'
COMMAND = None
CMD_DB = new_database('quote')
CMD = Query()


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    search = CMD_DB.get(CMD.cmd == message)
    if search is None:
        return
    if 'text' in search:
        bot.sendMessage(search['text'],
                        thread_id=thread_id, thread_type=thread_type)
    elif 'image' in search:
        bot.sendRemoteImage(search['image'],
                            thread_id=thread_id, thread_type=thread_type)
