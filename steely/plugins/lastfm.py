#!/usr/bin/env python3

"""
`[]` optional, `<>` mandatory

.np set <username>
.np [username]
.np collage [username]
.np top [overall|7day|1month|3month|6month|12month]
.np list
"""


import requests
import json
from tinydb import TinyDB, Query
from operator import itemgetter
from steelybot import config
from contextlib import suppress


COMMAND = '.np'
USERDB = TinyDB('lastfm.json')
USER = Query()
API_BASE = "http://ws.audioscrobbler.com/2.0/"
COLLAGE_BASE = "http://www.tapmusic.net/collage.php/"
SHORTENER_BASE = 'https://www.googleapis.com/urlshortener/v1/url'


## helpers ##
def get_np(user):
    params = {'method': 'user.getRecentTracks',
              'user': user,
              'api_key': config.LASTFM_API_KEY,
              'limit': '1',
              'format': 'json'}
    response = requests.get(API_BASE, params=params)
    return response.json()["recenttracks"]["track"][0]


def get_info(user):
    params = {'method': 'user.getInfo',
              'user': user,
              'api_key': config.LASTFM_API_KEY,
              'limit': '1',
              'format': 'json'}
    response = requests.get(API_BASE, params=params)
    return response.json()["user"]


def get_top(user, period):
    params = {'method': 'user.getTopArtists',
              'api_key': config.LASTFM_API_KEY,
              'period': period,
              'user': user,
              'limit': "6",
              'format': 'json'}
    response = requests.get(API_BASE, params=params)
    return response.json()["topartists"]["artist"]


def get_tags(artist, track):
    params = {'method': 'artist.gettoptags',
              'api_key': config.LASTFM_API_KEY,
              'artist': artist,
              'format': 'json'}
    response = requests.get(API_BASE, params=params)
    for tag in response.json()['toptags']['tag'][:3]:
        tag_name = tag['name']
        if tag_name in ('seen live', ):
            continue
        yield tag_name.lower()


def make_collage(author_id, user):
    params = {'user': user,
              'type': '7day',
              'size': '3x3',
              'caption': 'true'}
    image_res = requests.get(COLLAGE_BASE, params=params)
    image = image_res.content
    image_path = '/tmp/{}.jpg'.format(author_id)
    with open(image_path, 'wb') as image_file:
        image_file.write(image)
    return image_path


def shorten_url(url):
    data = {'longUrl': url}
    params = {'key': config.SHORTENER_API_KEY}
    headers = {'content-type': 'application/json'}
    response = requests.post(SHORTENER_BASE, params=params,
        data=json.dumps(data), headers=headers)
    return response.json()["id"]


def is_online(user):
    try:
        latest_track_obj = get_np(user)
    except IndexError:
        return False
    return "@attr" in latest_track_obj and \
        "nowplaying" in latest_track_obj["@attr"]


## subcommands ##
def send_top(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    username = USERDB.get(USER.id == author_id)["username"]
    periods = ("overall", "7day", "1month", "3month", "6month", "12month")
    if not message_parts:
        period = "7day"
    elif message_parts[0] in periods:
        period = message_parts[0]
    else:
        bot.sendMessage("period must be one of `{}`".format(", ".join(periods)),
            thread_id=thread_id, thread_type=thread_type)
        return
    artists, string = [], "```"
    for artist in get_top(username, period):
        artists.append((artist["name"], int(artist["playcount"])))
    max_artist = max(len(artist) for artist, plays in artists)
    max_plays = max(len(str(plays)) for artists, plays in artists)
    for artist, playcount in artists:
        string += "\n{artist:<{max_artist}} {playcount:>{max_plays}}".format_map(locals())
    bot.sendMessage(string + "```", thread_id=thread_id, thread_type=thread_type)


def send_collage(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if not message_parts:
        username = USERDB.get(USER.id == author_id)["username"]
    else:
        username = message_parts[0]
    bot.sendLocalImage(make_collage(author_id, username),
                       message=None,
                       thread_id=thread_id,
                       thread_type=thread_type)


def send_list(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    max_username = max(len(user["username"]) for user in USERDB.all())
    stats = []
    for user in USERDB.all():
        username = user["username"]
        playcount = int(get_info(username)["playcount"])
        stats.append((is_online(username), username, playcount))
    message = "```\n"
    for online, username, playcount in sorted(stats, key=itemgetter(0, 2), reverse=True):
        online_str = " ♬"[online]
        message += "{online_str} {username:<{max_username}} {playcount:>6,}\n".format_map(locals())
    message += "```"
    bot.sendMessage(message,
                    thread_id=thread_id, thread_type=thread_type)


def send_np(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    user = USERDB.get(USER.id == author_id)
    if message_parts:
        username = message_parts[0]
    elif user:
        username = user['username']
    else:
        bot.sendMessage('include username please or use .np set',
                        thread_id=thread_id, thread_type=thread_type)
        return
    latest_track_obj = get_np(username)
    album = latest_track_obj["album"]["#text"]
    artist = latest_track_obj["artist"]["#text"]
    track = latest_track_obj["name"]
    tags = ", ".join(get_tags(artist, track))
    link = shorten_url(latest_track_obj["url"])
    with suppress(ValueError):
        image = latest_track_obj["image"][2]["#text"]
        bot.sendRemoteImage(image, thread_id=thread_id, thread_type=thread_type)
    is_was = "is" if "@attr" in latest_track_obj and \
        "nowplaying" in latest_track_obj["@attr"] else "was"
    bot.sendMessage("{username} {is_was} playing `{track}` by {artist}\n" \
                    "tags: {tags}\n{link}".format_map(locals()),
                    thread_id=thread_id, thread_type=thread_type)


def set_username(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if not message_parts:
        bot.sendMessage('provide a username',
                thread_id=thread_id, thread_type=thread_type)
        return
    username = message_parts[0]
    if not USERDB.search(USER.id == author_id):
        USERDB.insert({'id': author_id, 'username': username})
        bot.sendMessage('good egg', thread_id=thread_id, thread_type=thread_type)
    else:
        USERDB.update({'username': username}, USER.id == author_id)
        bot.sendMessage('updated egg', thread_id=thread_id, thread_type=thread_type)


SUBCOMMANDS = {
    'collage': send_collage,
    'top': send_top,
    'list': send_list,
    'set': set_username
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message_parts = message.split()
    if message_parts and message_parts[0] in SUBCOMMANDS:
        SUBCOMMANDS[message_parts[0]](bot, author_id, message_parts[1:], thread_id, thread_type, **kwargs)
    else:
        send_np(bot, author_id, message_parts, thread_id, thread_type, **kwargs)
