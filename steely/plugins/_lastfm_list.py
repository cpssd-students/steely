from plugins._lastfm_helpers import *
from operator import itemgetter
from formatting import *


def parse_onlines(async_responses):
    ''' take a list of Futures() for who's online, wait for each to complete,
        and yield if each user is online or not
    '''
    for async_response in async_responses:
        response = async_response.result()
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
        if not "user" in response_obj:
            yield 0
            continue
        username = response_obj["user"]["name"]
        playcount = int(response_obj["user"]["playcount"])
        yield playcount


def main(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    playcount_asyncrequests = get_lastfm_asyncrequest_list('user.getInfo')
    online_aysncrequests = get_lastfm_asyncrequest_list('user.getRecentTracks')
    playcounts = parse_playcounts(playcount_asyncrequests)
    onlines = parse_onlines(online_aysncrequests)
    usernames = [user["username"] for user in USERDB.all()]
    max_username = max(len(username) for username in usernames)
    stats = zip(list(onlines), usernames, list(playcounts))
    message = ""
    for online, username, playcount in sorted(stats, key=itemgetter(0, 2), reverse=True):
        if playcount == 0:
            continue
        online_str = " ♬"[online]
        message += f"{online_str} {username:<{max_username}} {playcount:>6,}\n"
    bot.sendMessage(code_block(message), thread_id=thread_id,
                    thread_type=thread_type)
