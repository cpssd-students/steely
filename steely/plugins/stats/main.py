#!/usr/bin/env python3

import logging
from operator import itemgetter

from tinydb import Query
from tinydb.operations import increment

from utils import new_database
from plugin import PluginManager, create_plugin
from message import SteelyMessage
from formatting import code_block

__author__ = 'sentriz'
COMMAND = None
CMD_DB = new_database('stats')
CMD = Query()
TILDA_DB = new_database('quote')
TILDA = Query()
COMMAND_IDENTIFIERS = set(['.', '~', '/'])

LOGGER = logging.getLogger("plugins.stats")
LOGGER.setLevel(logging.INFO)

HELP_STR = '''TODO'''
PLUGIN = create_plugin(name="stats", author="sentriz", help=HELP_STR)

DEFAULT_LIST_SIZE = 10

def first_word_of(message):
    if ' ' in message:
        message = message.split()[0]
    return message


def is_tilda_command(command):
    return bool(TILDA_DB.search(TILDA.cmd == command))


def looks_like_command(command):
    return any(command.startswith(char) for char in COMMAND_IDENTIFIERS)


def strip_command(message):
    return message[1:] if message[0] in COMMAND_IDENTIFIERS else message


def is_old_style_command(command, plugins):
    if not looks_like_command(command):
        return False
    if strip_command(command) in plugins:
        return True
    elif is_tilda_command(command):
        return True
    return False


def is_new_style_command(message):
    message = strip_command(message)
    return (PluginManager.get_listener_for_command(message, logger=LOGGER) is not None)

# Records usage of a specific command.
# `command` can be a single- or multi-token string, but regardless should start
# with a command identifier (eg. "/").
# For example, `command` could be any of ["/np", "/np set", "/np set iandioch"].
# if `command` is a multi-token string, N prefixes will be recorded; eg. for
# the `command` "/np set iandioch", if N >= 3, all of ["/np set iandioch",
# "/np set", "/np"] will be incremented in the DB. If N=1, only "/np" will be
# incremented.


def record_command_usage(command, N=2):
    LOGGER.info(f'Incrementing stat for command usage {command} with N={N}')
    command_parts = command.split()
    for i in range(min(len(command_parts), N)):
        command_prefix = ' '.join(command_parts[:i + 1])
        stat_search = CMD_DB.get(CMD.command == command_prefix)
        if not stat_search:
            CMD_DB.insert({'command': command_prefix, 'count': 1})
        else:
            CMD_DB.update(increment('count'), CMD.command == command_prefix)


@PLUGIN.listen()
def listen_for_usage(bot, message: SteelyMessage, **kwargs):
    if not len(message.text) or not message.text[0] in COMMAND_IDENTIFIERS:
        return
    command = first_word_of(message.text)
    plugins = bot.plugins
    if not (is_old_style_command(command, plugins) or
            is_new_style_command(message.text)):
        return
    record_command_usage(message.text)

def get_all_stats():
    def parse_stats(stats):
        for stat in CMD_DB.all():
            yield stat['command'], stat['count']
    return list(parse_stats(CMD_DB))

def format_stats(title_str, sorted_stats):
    max_command = max(len(command) for command, count in sorted_stats)
    response = f'{title_str}\n――――――\n'
    for command, count in sorted_stats:
        if count == 100:
            representation = '💯'
        else:
            representation = count
        response += f'{command:<{max_command}} {representation:>3,}\n'
    return response



@PLUGIN.listen("stats top [n]")
def emit_top_stats(bot, message: SteelyMessage, **kwargs):
    def sort_stats(stats):
        return sorted(stats, key=itemgetter(1), reverse=True)

    n = DEFAULT_LIST_SIZE 
    if 'n' in kwargs and kwargs['n'] != '':
        n = int(kwargs['n'])
    stats = sort_stats(get_all_stats())
    n = min(n, len(stats))
    response = format_stats(f'top {n}', stats[:n])
    bot.sendMessage(code_block(response),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)

@PLUGIN.listen("stats [n]")
def emit_default_stats(bot, message: SteelyMessage, **kwargs):
    emit_top_stats(bot, message, **kwargs)

@PLUGIN.listen("stats bottom [n]")
def emit_bottom_stats(bot, message: SteelyMessage, **kwargs):
    def sort_stats(stats):
        return sorted(stats, key=itemgetter(1))

    n = DEFAULT_LIST_SIZE 
    if 'n' in kwargs and kwargs['n'] != '':
        n = int(kwargs['n'])
    stats = sort_stats(get_all_stats())
    n = min(n, len(stats))
    response = format_stats(f'bottom {n}', stats[:n])
    bot.sendMessage(code_block(response),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)

@PLUGIN.listen("stats bottom <n> real")
def emit_real_bottom_stats(bot, message: SteelyMessage, **kwargs):
    def is_real_stat(stat):
        return len(stat) and stat[0] == '/' and len(stat.split(' ')) == 1 and '@' not in stat
    def sort_and_filter_stats(stats):
        filtered_stats = [stat for stat in stats if is_real_stat(stat[0])]
        return sorted(filtered_stats, key=itemgetter(1))

    n = DEFAULT_LIST_SIZE 
    if 'n' in kwargs and kwargs['n'] != '':
        n = int(kwargs['n'])
    stats = sort_and_filter_stats(get_all_stats())
    n = min(n, len(stats))
    response = format_stats(f'bottom {n}', stats[:n])
    bot.sendMessage(code_block(response),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)
