#!/usr/bin/env python3

'''
show plugin stats
'''


from tinydb import TinyDB, Query
from operator import itemgetter


__author__ = 'sentriz'
COMMAND = '.stats'
CMD_DB = TinyDB('stats.json')
CMD = Query()
LIMIT = 10


def parse_stats(stats):
    for stat in CMD_DB.all():
        yield stat['command'], stat['count']


def sort_stats(stats):
    return sorted(stats, key=itemgetter(1), reverse=True)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    clean_stats = list(parse_stats(CMD_DB))[:LIMIT]
    max_command = max(len(command) for command, count in clean_stats)
    sorted_stats = sort_stats(clean_stats)
    message = f'```\ntop {LIMIT}\n――――――\n'
    for command, count in sorted_stats:
        message += f'{command:<{max_command}} {count:>3,}\n'
    message += '```'
    bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
