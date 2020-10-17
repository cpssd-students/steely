from plugin import create_plugin, PluginManager
from utils import new_database
from tinydb import Query

plugin = create_plugin(name='nw', author='iandioch', help='todo')

USERDB = None
USER = Query()
LETTERBOXD_RSS_ADDRESS = 'https://letterboxd.com/{}/rss/'
rss = None

@plugin.setup()
def plugin_setup():
    global USERDB, rss
    import feedparser
    rss = feedparser

    USERDB = new_database('letterboxd')

@plugin.listen(command='nw')
def root_command(bot, author_id, message, thread_id, thread_type, **kwargs):
    print(author_id, message)

@plugin.listen(command='nw set')
def set_command(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message or not len(message):
        print('no username provided.')
        return
    username = message.split(' ')[0]
    if not USERDB.search(USER.id == author_id):
        USERDB.insert({'id': author_id, 'username': username})
        bot.sendMessage('good egg', thread_id=thread_id,
                        thread_type=thread_type)
    else:
        USERDB.update({'username': username}, USER.id == author_id)
        bot.sendMessage('updated egg', thread_id=thread_id,
                        thread_type=thread_type)

@plugin.listen(command='nw help')
def help_command(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(plugin.help, thread_id=thread_id, thread_type=thread_type)
