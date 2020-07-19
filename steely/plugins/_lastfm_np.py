from plugins._lastfm_helpers import *
import json
from contextlib import suppress
from formatting import *
from paths import CONFIG


def parse_tags(response):
    ''' parse artist.getTopTags and return the top 3 tags '''
    for tag in response.json()['toptags']['tag'][:3]:
        tag_name = tag['name']
        if tag_name in ('seen live', ):
            continue
        yield tag_name.lower()


def absolute_short_url(relative):
    return CONFIG.FLASKNASC_HOST + relative


# Try to get a short URL. If the URL shortener service isn't responding, just
# return the original long URL.
def maybe_get_short_url(long_url):
    try:
        params = {
            'key': CONFIG.FLASKNASC_KEY,
            'address': long_url
        }
        path = CONFIG.FLASKNASC_HOST + "/new/" + CONFIG.FLASKNASC_USER
        response = requests.get(path, params=params)
        return absolute_short_url(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error while trying to shorten URL for .np:')
        print(e)
        return long_url


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
    latest_track_obj = get_lastfm_request("user.getRecentTracks",
                                          user=username, limit=1).json()["recenttracks"]["track"][0]
    album = latest_track_obj["album"]["#text"]
    artist = latest_track_obj["artist"]["#text"]
    track = latest_track_obj["name"]
    tag_response = get_lastfm_request("artist.getTopTags", artist=artist)
    tags = ', '.join(parse_tags(tag_response))
    link = maybe_get_short_url(latest_track_obj["url"])
    with suppress(ValueError):
        image = latest_track_obj["image"][2]["#text"]
        bot.sendRemoteImage(image, thread_id=thread_id,
                            thread_type=thread_type)
    is_was = "is" if "@attr" in latest_track_obj and \
        "nowplaying" in latest_track_obj["@attr"] else "was"
    tags_or_no = f"\ntags: {tags}" if tags else ''
    bot.sendMessage(f"{username} {is_was} playing {italic(track)} by {bold(artist)}" +
                    f"{tags_or_no}\n{link}",
                    thread_id=thread_id, thread_type=thread_type)
