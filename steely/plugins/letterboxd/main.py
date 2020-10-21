from plugin import create_plugin, PluginManager
from message import SteelyMessage
from utils import new_database
from tinydb import Query
from paths import CONFIG
from formatting import *
import requests

HELP_STR = """'Now Watching' command, to give info on what films someone has
recently watched, based on letterboxd.com activity."""

plugin = create_plugin(name='nw', author='iandioch', help=HELP_STR)

USERDB = None
USER = Query()
LETTERBOXD_RSS_ADDRESS = 'https://letterboxd.com/{}/rss/'
rss = None


def absolute_short_url(relative):
    return CONFIG.FLASKNASC_HOST + relative


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


def get_most_recent_film(username):
    print('Getting most recent film for {}'.format(username))
    # TODO(iandioch): This returns the first thing in the feed, based on
    # <pubDate> (when the user added it), not based on
    # <letterboxd:watchedDate> (when the user specified they watched it).
    feed = rss.parse(LETTERBOXD_RSS_ADDRESS.format(username))
    if not len(feed.entries):
        return None, None, None
    item = feed.entries[0]
    url = maybe_get_short_url(item.link)
    title = item.title  # includes film title, year, and maybe a 1-5 star review
    desc = item.description  # includes either watch date, or fuller text review
    date_parts = item.published_parsed
    date_str = '{}/{}/{}'.format(date_parts.tm_year,
                                 date_parts.tm_mon, date_parts.tm_mday)
    return title, date_str, url


@plugin.setup()
def plugin_setup():
    global USERDB, rss
    import feedparser
    rss = feedparser

    USERDB = new_database('letterboxd')


@plugin.listen(command='nw [username]')
def root_command(bot, message: SteelyMessage, **kwargs):
    user = USERDB.get(USER.id == message.author_id)
    if 'username' in kwargs:
        username = kwargs['username']
    elif user:
        username = user['username']
    else:
        bot.sendMessage(f'include username please or use `/nw set`',
                        thread_id=message.thread_id,
                        thread_type=message.thread_type)
        return

    title, date_str, url = get_most_recent_film(username)
    if title is None:
        bot.sendMessage(f'Could not load most recent film for {username}.',
                        thread_id=message.thread_id,
                        thread_type=message.thread_type)
        return

    bot.sendMessage(f"{username} added {italic(title)} on {date_str}\n{url}",
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)


@plugin.listen(command='nw set <username>')
def set_command(bot, message: SteelyMessage, **kwargs):
    if 'username' not in kwargs or not len(kwargs['username']):
        bot.sendMessage('no username provided', thread_id=message.thread_id,
                        thread_type=message.thread_type)
        return
    username = kwargs['username']
    if not USERDB.search(USER.id == message.author_id):
        USERDB.insert({'id': message.author_id, 'username': username})
        bot.sendMessage('good egg, you\'re now {}'.format(username),
                        thread_id=message.thread_id,
                        thread_type=message.thread_type)
    else:
        USERDB.update({'username': username}, USER.id == message.author_id)
        bot.sendMessage('updated egg, you\'re now {}'.format(username),
                        thread_id=message.thread_id,
                        thread_type=message.thread_type)


@plugin.listen(command='nw help')
def help_command(bot, message: SteelyMessage, **kwargs):
    bot.sendMessage(plugin.help, thread_id=thread_id, thread_type=thread_type)
    bot.sendMessage('\n'.join(("/" + command) for command in plugin.commands),
                    thread_id=message.thread_id, thread_type=message.thread_type)
