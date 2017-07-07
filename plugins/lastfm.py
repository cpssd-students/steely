#!/usr/bin/env python3


import requests
from tinydb import TinyDB, Query
from operator import itemgetter
from steelybot import config


COMMAND = '.np'
USERDB = TinyDB('lastfm.json')
USER = Query()
API_BASE = "http://ws.audioscrobbler.com/2.0/"
COLLAGE_BASE = "http://www.tapmusic.net/collage.php/"


## helpers ##
def get_np(user):
    params = {'method': 'user.getRecentTracks',
              'user': user,
              'api_key': config.LASTFM_API_KEY,
              'limit': '1',
              'format': 'json'}
    response = requests.get(API_BASE, params=params)
    return response.json()["recenttracks"]["track"]


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
              'type': '1month',
              'size': '3x3',
              'caption': 'true'}
    image_res = requests.get(COLLAGE_BASE, params=params)
    image = image_res.content
    image_path = '/tmp/{}.jpg'.format(author_id)
    with open(image_path, 'wb') as image_file:
        image_file.write(image)
    return image_path


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
        stats.append((lastfm, get_playcount(lastfm)))
    message = "```\n"
    for lastfm, playcount in sorted(stats, key=itemgetter(1), reverse=True):
        message += "{:<{max_lastfm}} {:>6,}\n".format(lastfm, playcount, max_lastfm=max_lastfm)
    message += "```"
    bot.sendMessage(message,
                    thread_id=thread_id, thread_type=thread_type)


def send_np(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    user = USERDB.get(USER.fb_id == author_id)
    if message_parts:
        lastfm = message_parts[0]
    elif user:
        lastfm = user['lastfm']
    else:
        bot.sendMessage('include username please or use .np set',
                        thread_id=thread_id, thread_type=thread_type)
        return
    latest_track_obj = get_np(lastfm)[0]
    album = latest_track_obj["album"]["#text"]
    artist = latest_track_obj["artist"]["#text"]
    track = latest_track_obj["name"]
    tags = ", ".join(get_tags(artist, track))
    bot.sendMessage("{lastfm} is playing '{track}' by {artist} from \"{album}\"\n" \
                    "tags: {tags}".format_map(locals()),
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
    'set': set_username
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message_parts = message.split()
    if message_parts and message_parts[0] in SUBCOMMANDS:
        SUBCOMMANDS[message_parts[0]](bot, author_id, message_parts[1:], thread_id, thread_type, **kwargs)
    else:
        send_np(bot, author_id, message_parts, thread_id, thread_type, **kwargs)
