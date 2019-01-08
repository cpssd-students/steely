#!/usr/bin/env python3

'''
show plugin stats
'''


from formatting import *
from operator import itemgetter
from tinydb import Query
from utils import new_database


__author__ = 'sentriz'
COMMAND = 'stats'
CMD_DB = new_database('stats')
CMD = Query()
LIMIT = 10


def parse_stats(stats):
    for stat in CMD_DB.all():
        yield stat['command'], stat['count']


def sort_stats(stats):
    return sorted(stats, key=itemgetter(1), reverse=True)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    clean_stats = list(parse_stats(CMD_DB))
    sorted_stats = sort_stats(clean_stats)[:LIMIT]
    max_command = max(len(command) for command, count in sorted_stats)
    message = f'top {LIMIT}\n――――――\n'
    for command, count in sorted_stats:
        if count == 100:
            representation = '💯'
        else:
            representation = count
        message += f'{command:<{max_command}} {representation:>3,}\n'
    bot.sendMessage(code_block(message), thread_id=thread_id,
                    thread_type=thread_type)
