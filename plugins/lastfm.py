import requests
from tinydb import TinyDB, Query
from steelybot import config

COMMAND = '.np'
USERDB = TinyDB('../lastfm.json')
user = Query()

def get_np(apikey, user):
    base = "http://ws.audioscrobbler.com/2.0/"
    url = "?method=user.getrecenttracks&user={}&api_key={}&limit=2&format=json".format(user, apikey)
    res = requests.get(base+url)
    return res.json()["recenttracks"]["track"][0]

def extract_song(user):
    try:
        response = get_np(config.LASTFM_API_KEY, user)
    except requests.exceptions.RequestException:
        return 'failed to retrieve now playing information'
    artist = response['artist']['#text']
    song = response['name']
    return '{} is playing {} by {}'.format(user, song, artist)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    m = message.split()
    if not message:
        s = USERDB.search(user.fb_id == author_id)
        if len(s) != 0:
            lastfm_name = s[0]['lastfm']
            bot.sendMessage(extract_song(lastfm_name), thread_id=thread_id, thread_type=thread_type)
        else:
            bot.sendMessage('include username please or use .np set', thread_id=thread_id, thread_type=thread_type)
        return

    elif m[0] == 'set' and len(m) == 2:
        if len(USERDB.search(user.fb_id == author_id)) == 0:
            USERDB.insert({"fb_id" : author_id, "lastfm" : m[1]})
            bot.sendMessage('good egg', thread_id=thread_id, thread_type=thread_type)
        else:
            USERDB.update({"lastfm" : m[1]}, user.fb_id == author_id)
            bot.sendMessage('updated egg', thread_id=thread_id, thread_type=thread_type)
        return
    else: 
        bot.sendMessage(extract_song(message), thread_id=thread_id, thread_type=thread_type)
        return
