#!/usr/bin/env python3

import logging

from tinydb import Query
from tinydb.operations import increment
from utils import new_database

from plugin import PluginManager

__author__ = 'sentriz'
COMMAND = None
CMD_DB = new_database('stats')
CMD = Query()
TILDA_DB = new_database('quote')
TILDA = Query()
COMMAND_IDENTIFIERS = set(['.', '~', '/'])

LOGGER = logging.getLogger("plugins.stats")
LOGGER.setLevel(logging.INFO)


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


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not len(message) or not message[0] in COMMAND_IDENTIFIERS:
        return
    command = first_word_of(message)
    plugins = bot.plugins
    if not (is_old_style_command(command, plugins) or
            is_new_style_command(message)):
        return
    record_command_usage(message)
