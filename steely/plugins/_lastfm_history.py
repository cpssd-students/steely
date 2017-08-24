#!/usr/bin/env python3


from plugins._lastfm_helpers import *
from operator import itemgetter


def time_or_now(track):
    if 'date' in track:
        return parsed_time(track['date']['#text'])
    return 'now'


def parsed_time(time_string):
    return time_string.split(', ')[1]


def parsed_response(response):
    for track in response['recenttracks']['track']:
        yield time_or_now(track), \
              track['artist']['#text'], \
              track['name']


def gen_reply_string(response):
    yield '```'
    for time, artist, track in parsed_response(response):
        yield f'{time:>5} {artist:<15.15} {track:.25}'
    yield '```'


def main(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if message_parts:
        username = message_parts[0]
    else:
        username = USERDB.get(USER.id == author_id)['username']
    response = get_lastfm_request('user.getRecentTracks', user=username, limit=8).json()
    reply = gen_reply_string(response)
    bot.sendMessage('\n'.join(reply), thread_id=thread_id, thread_type=thread_type)
