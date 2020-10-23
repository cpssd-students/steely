import json
import random

from plugin import create_plugin
from message import SteelyMessage

HELP_STR = """
Request your favourite bible quotes, right to the chat.
"""
BIBLE_FILE = "plugins/bible/en_kjv.json"

plugin = create_plugin(name='bible', author='CianLR', help=HELP_STR)
bible = None

@plugin.setup()
def plugin_setup():
    global bible
    # This can be obtained from https://github.com/thiagobodruk/bible
    bible = json.loads(open(BIBLE_FILE).read().decode('utf-8-sig'))


@plugin.listen(command='bible help')
def help_command(bot, message: SteelyMessage, **kwargs):
    bot.sendMessage(
            "Simply call /bible to receive your daily dose of the good book",
            thread_id=message.thread_id, thread_type=message.thread_type)


def get_quote(book, chapter, verse):
    return "{}\n - {} {}:{}".format(
            bible[book]["chapters"][chapter][verse],
            bible[book]["book"], chapter, verse)


@plugin.listen(command='bible [passage]')
def passage_command(bot, message: SteelyMessage, **kwargs):
    if 'passage' not in kwargs:
        book = random.randrange(len(bible))
        chapter = random.randrange(len(bible[book]["chapters"]))
        verse = random.randrange(len(bible[book]["chapters"][chapter]))
        bot.sendMessage(
                get_quote(book, chapter, verse),
                thread_id=message.thread_id, thread_type=message.thread_type)
    else:
        pass  # TODO(cianlr): Implement.
