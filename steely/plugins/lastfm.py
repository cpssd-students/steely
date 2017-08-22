#!/usr/bin/env python3
"""
np does last fm stuff

set your username:
.np set <username>

check whats your listening to:
.np [username]
.np top <overall|7day|1month|3month|6month|12month> [username]

make a collage:
.np collage <overall|7day|1month|3month|6month|12month> [username]

scrobbles:
.np list
"""


import requests
import timeit
from requests_futures.sessions import FuturesSession
import json
from tinydb import TinyDB, Query
from operator import itemgetter
from steelybot import config
from contextlib import suppress


COMMAND = '.np'
USERDB = TinyDB('lastfm.json')
USER = Query()
SESSION = FuturesSession(max_workers=100)
API_BASE = "http://ws.audioscrobbler.com/2.0/"
COLLAGE_BASE = "http://www.tapmusic.net/collage.php/"
SHORTENER_BASE = 'https://www.googleapis.com/urlshortener/v1/url'
PERIODS = ("7day", "1month", "3month", "6month", "12month", "overall")


def get_collage(author_id, user, period):
    params = {'user': user,
              'type': period,
              'size': '3x3',
              'caption': 'true'}
    image_res = requests.get(COLLAGE_BASE, params=params)
    image = image_res.content
    image_path = f'/tmp/{author_id}.jpg'
    with open(image_path, 'wb') as image_file:
        image_file.write(image)
    return image_path


def get_short_url(url):
    data = {'longUrl': url}
    params = {'key': config.SHORTENER_API_KEY}
    headers = {'content-type': 'application/json'}
    response = requests.post(SHORTENER_BASE, params=params,
        data=json.dumps(data), headers=headers)
    return response.json()["id"]


# requesting
def get_lastfm_request(method, **kwargs):
    ''' make a normal python request to the last.fm api
        return a Response()
    '''
    params = {'method': method,
              'api_key': config.LASTFM_API_KEY,
              'format': 'json'}
    params.update(kwargs)
    return requests.get(API_BASE, params=params)


def get_lastfm_asyncrequest(method, **kwargs):
    ''' make an aysnc request using a requests_futures FuturesSession
        to the last.fm api
        return a Future()
    '''
    params = {'method': method,
              'api_key': config.LASTFM_API_KEY,
              'format': 'json'}
    params.update(kwargs)
    return SESSION.get(API_BASE, params=params)


def get_lastfm_asyncrequest_list(method, **kwargs):
    ''' make a big list of running Futures()
    '''
    for user in USERDB.all():
        username = user["username"]
        yield get_lastfm_asyncrequest(method,
            user=username, limit=1, **kwargs)


# parsing
def parse_onlines(async_responses):
    ''' take a list of Futures() for who's online, wait for each to complete,
        and yield if each user is online or not
    '''
    for async_response in async_responses:
        response = async_response.result()
        # username = response.json()["recenttracks"]["@attr"]["user"]
        try:
            latest_track_obj = response.json()["recenttracks"]["track"][0]
        except IndexError:
            yield False
        else:
            yield "@attr" in latest_track_obj and \
                    "nowplaying" in latest_track_obj["@attr"]


def parse_playcounts(async_responses):
    ''' take a list of Futures() for playcounts, wait for each to complete,
        and yield the playcount
    '''
    for async_response in async_responses:
        response = async_response.result()
        response_obj = response.json()
        username = response_obj["user"]["name"]
        playcount = int(response_obj["user"]["playcount"])
        yield playcount


def parse_tags(response):
    ''' should be using the built in lfm gette
    '''
    for tag in response.json()['toptags']['tag'][:3]:
        tag_name = tag['name']
        if tag_name in ('seen live', ):
            continue
        yield tag_name.lower()


# commands
def send_top(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if not message_parts or message_parts[0] not in PERIODS:
        bot.sendMessage('usage: .np top <period> [username]',
            thread_id=thread_id, thread_type=thread_type)
        return
    else:
        period = message_parts[0]
    if len(message_parts) == 2:
        username = message_parts[1]
    else:
        username = USERDB.get(USER.id == author_id)["username"]
    artists, string = [], "```"
    for artist in get_top(username, period):
        artists.append((artist["name"], int(artist["playcount"])))
    max_artist = max(len(artist) for artist, plays in artists)
    max_plays = max(len(str(plays)) for artists, plays in artists)
    for artist, playcount in artists:
        string += f"\n{artist:<{max_artist}} {playcount:>{max_plays}}"
    bot.sendMessage(string + "```", thread_id=thread_id, thread_type=thread_type)


def send_collage(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if not message_parts or message_parts[0] not in PERIODS:
        bot.sendMessage('usage: .np collage <period> [username]',
            thread_id=thread_id, thread_type=thread_type)
        return
    else:
        period = message_parts[0]
    if len(message_parts) == 2:
        username = message_parts[1]
    else:
        username = USERDB.get(USER.id == author_id)["username"]
    bot.sendLocalImage(get_collage(author_id, username, period),
                       message=None, thread_id=thread_id, thread_type=thread_type)


def send_list(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    playcount_asyncrequests = get_lastfm_asyncrequest_list('user.getInfo')
    online_aysncrequests = get_lastfm_asyncrequest_list('user.getRecentTracks')
    playcounts = parse_playcounts(playcount_asyncrequests)
    onlines = parse_onlines(online_aysncrequests)
    usernames = [user["username"] for user in USERDB.all()]
    max_username = max(len(username) for username in usernames)
    stats = zip(list(onlines), usernames, list(playcounts))
    message = "```\n"
    for online, username, playcount in sorted(stats, key=itemgetter(0, 2), reverse=True):
        online_str = " ♬"[online]
        message += f"{online_str} {username:<{max_username}} {playcount:>6,}\n"
    message += "```"
    bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)


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
    latest_track_obj = get_lastfm_request("user.getRecentTracks",
        user=username, limit=1).json()["recenttracks"]["track"][0]
    album = latest_track_obj["album"]["#text"]
    artist = latest_track_obj["artist"]["#text"]
    track = latest_track_obj["name"]
    tag_response = get_lastfm_request("artist.getTopTags", artist=artist)
    tags = ', '.join(parse_tags(tag_response))
    link = get_short_url(latest_track_obj["url"])
    with suppress(ValueError):
        image = latest_track_obj["image"][2]["#text"]
        bot.sendRemoteImage(image, thread_id=thread_id, thread_type=thread_type)
    is_was = "is" if "@attr" in latest_track_obj and \
        "nowplaying" in latest_track_obj["@attr"] else "was"
    tags_or_no = f"\ntags: {tags}" if tags else ''
    bot.sendMessage(f"{username} {is_was} playing `{track}` by {artist}" + \
                    f"{tags_or_no}\n{link}",
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
