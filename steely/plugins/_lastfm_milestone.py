from plugins._lastfm_helpers import *
import json
from contextlib import suppress
from formatting import *
from steely import config


def gen_milestones():
    base = (10, 25, 50, 75)
    i = 1
    while i < 10**10:
        for n in base:
            yield n * i
        i *= 10


def get_distance_and_milestone(scrobbles):
    for milestone in gen_milestones():
        if scrobbles < milestone:
            break
    distance = milestone - scrobbles
    return distance, milestone


def main(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    user = USERDB.get(USER.id == author_id)
    if message_parts:
        username = message_parts[0]
    elif user:
        username = user['username']
    else:
        bot.sendMessage(f'include username please or use {COMMAND} set',
                        thread_id=thread_id, thread_type=thread_type)
        return
    scrobbles = get_lastfm_request("user.getInfo",
                                   user=username) \
                    .json() \
                    ['user']['playcount']
    distance, milestone = get_distance_and_milestone(scrobbles)
    bot.sendMessage(f"{username} is {distance:,} scrobbles away from their next milestone of *{milestone:,}*",
                    thread_id=thread_id, thread_type=thread_type)
