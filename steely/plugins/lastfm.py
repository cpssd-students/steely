#!/usr/bin/env python3
from plugins._lastfm_helpers import *
from plugins import _lastfm_collage
from plugins import _lastfm_history
from plugins import _lastfm_list
from plugins import _lastfm_milestone
from plugins import _lastfm_np
from plugins import _lastfm_set
from plugins import _lastfm_top


__author__ = ('alexkraak', 'sentriz')
SUBCOMMANDS = {
    'collage':   _lastfm_collage.main,
    'history':   _lastfm_history.main,
    'list':      _lastfm_list.main,
    'milestone': _lastfm_milestone.main,
    'set':       _lastfm_set.main,
    'top':       _lastfm_top.main,
}

__doc__ = f"""
np does last fm stuff

set your username:
{COMMAND} set <username>

check what you're listening to:
{COMMAND} [username]
{COMMAND} top <overall|7day|1month|3month|6month|12month> [username]
{COMMAND} history [username]

make a collage:
{COMMAND} collage <overall|7day|1month|3month|6month|12month> [username]

scrobbles:
{COMMAND} list

milestone:
{COMMAND} milestone
"""


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message_parts = message.split()
    if message_parts and message_parts[0] in SUBCOMMANDS:
        SUBCOMMANDS[message_parts[0]](
            bot, author_id, message_parts[1:], thread_id, thread_type, **kwargs)
    else:
        _lastfm_np.main(bot, author_id, message_parts,
                        thread_id, thread_type, **kwargs)
