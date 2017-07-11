#!/usr/bin/env python3


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


def get_playcount(user):
    params = {'method': 'user.getInfo',
              'user': user,
              'api_key': config.LASTFM_API_KEY,
              'limit': '1',
              'format': 'json'}
    response = requests.get(API_BASE, params=params)
    return int(response.json()["user"]["playcount"])


def get_tags(artist, track):
    params = {'method': 'artist.gettoptags',
              'api_key': config.LASTFM_API_KEY,
              'artist': artist,
              'user': 'alexkraak',
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
def send_collage(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if not message_parts:
        user = USERDB.get(USER.fb_id == author_id)["lastfm"]
    else:
        user = message_parts[0]
    bot.sendLocalImage(make_collage(author_id, user),
                       message=None,
                       thread_id=thread_id,
                       thread_type=thread_type)


def send_list(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    max_lastfm = max(len(user["lastfm"]) for user in USERDB.all())
    stats = []
    for user in USERDB.all():
        lastfm = user["lastfm"]
        stats.append((is_online(lastfm), lastfm, get_playcount(lastfm)))
    message = "```\n"
    for online, lastfm, playcount in sorted(stats, key=itemgetter(0, 2), reverse=True):
        online_str = " ♬"[online]
        message += "{online_str} {lastfm:<{max_lastfm}} {playcount:>6,}\n".format_map(locals())
    message += "```"
    bot.sendMessage(message,
                    thread_id=thread_id, thread_type=thread_type)


def send_np(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    user = USERDB.get(USER.fb_id == author_id)
    if message_parts:
        username = message_parts[0]
    elif user:
        username = user['lastfm']
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
    username = message_parts[1]
    if not USERDB.search(USER.fb_id == author_id):
        USERDB.insert({'fb_id': author_id, 'lastfm': username})
        bot.sendMessage('good egg', thread_id=thread_id, thread_type=thread_type)
    else:
        USERDB.update({'lastfm': username}, USER.fb_id == author_id)
        bot.sendMessage('updated egg', thread_id=thread_id, thread_type=thread_type)


SUBCOMMANDS = {
    'collage': send_collage,
    'list': send_list,
    'online': send_online,
    'set': set_username
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message_parts = message.split()
    if message_parts and message_parts[0] in SUBCOMMANDS:
        SUBCOMMANDS[message_parts[0]](bot, author_id, message_parts[1:], thread_id, thread_type, **kwargs)
    else:
        send_np(bot, author_id, message_parts, thread_id, thread_type, **kwargs)
