from plugins._lastfm_helpers import *
from formatting import *


def parse_top(response):
    ''' parse arist.getTopArtists and return the artist objects '''
    for artist in response.json()['topartists']['artist']:
        yield artist["name"], int(artist["playcount"])


def main(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if not message_parts or message_parts[0] not in PERIODS:
        period_string = '|'.join(PERIODS)
        bot.sendMessage(f'usage: .np top <{period_string}> [username]',
                        thread_id=thread_id, thread_type=thread_type)
        return
    else:
        period = message_parts[0]
    if len(message_parts) == 2:
        username = message_parts[1]
    else:
        username = USERDB.get(USER.id == author_id)["username"]
    artists = []
    topartsts_response = get_lastfm_request('user.getTopArtists',
                                            period=period, user=username, limit=8)
    artists = list(parse_top(topartsts_response))
    max_artist = max(len(artist) for artist, plays in artists)
    max_plays = max(len(str(plays)) for artists, plays in artists)
    output_lines = []
    for artist, playcount in artists:
        output_lines.append(f"{artist:<{max_artist}} {playcount:>{max_plays}}")
    bot.sendMessage(code_block("\n".join(output_lines)), thread_id=thread_id,
                    thread_type=thread_type)
