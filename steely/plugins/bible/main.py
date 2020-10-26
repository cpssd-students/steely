import json
import random
import requests

from plugin import create_plugin
from message import SteelyMessage

HELP_STR = """
Request your favourite bible quotes, right to the chat.

Usage:
    /bible - Random quote
    /bible Genesis 1:3 - Specific verse
    /bible help - This help text

    Verses are specified in the format {book} {chapter}:{verse}

TODO: Book acronyms, e.g. Gen -> Genesis
TODO: Verse ranges, e.g. Genesis 1:1-3
"""
BIBLE_FILE = "plugins/bible/en_kjv.json"
BIBLE_URL = 'https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json'

plugin = create_plugin(name='bible', author='CianLR', help=HELP_STR)
bible = None
book_to_index = {}

def make_book_to_index(bible):
    btoi = {}
    for i, book in enumerate(bible):
        btoi[book['name'].lower()] = i
    return btoi

@plugin.setup()
def plugin_setup():
    global bible, book_to_index
    try:
        bible = json.loads(open(BIBLE_FILE, encoding='utf-8-sig').read())
        book_to_index = make_book_to_index(bible)
        return
    except BaseException as e:
        pass
    # We've tried nothing and we're all out of ideas, download a new bible.
    try:
        bible = json.loads(
            requests.get(BIBLE_URL).content.decode('utf-8-sig'))
    except BaseException as e:
        return "Error loading bible: " + str(e)
    book_to_index = make_book_to_index(bible)
    with open(BIBLE_FILE, 'w') as f:
        json.dump(bible, f)


@plugin.listen(command='bible help')
def help_command(bot, message: SteelyMessage, **kwargs):
    bot.sendMessage(
            HELP_STR,
            thread_id=message.thread_id, thread_type=message.thread_type)


def is_valid_quote(book, chapter, verse):
    return (0 <= book < len(bible) and
            0 <= chapter < len(bible[book]['chapters']) and
            0 <= verse < len(bible[book]['chapters'][chapter]))


def get_quote(book, chapter, verse):
    return "{}\n - {} {}:{}".format(
            bible[book]["chapters"][chapter][verse],
            bible[book]["name"], chapter + 1, verse + 1)


def get_quote_from_ref(book_name, ref):
    if book_name.lower() not in book_to_index:
        return "Could not find book name: " + book_name
    book_i = book_to_index[book_name.lower()]
    if len(ref.split(':')) != 2:
        return 'Reference not in form "Book Chapter:Passage"'
    chapter, verse = ref.split(':')
    if not chapter.isnumeric():
        return "Chapter must be an int"
    chapter_i = int(chapter) - 1
    if not verse.isnumeric():
        return "Passage must be an int"
    verse_i = int(verse) - 1
    if not is_valid_quote(book_i, chapter_i, verse_i):
        return "Verse or chapter out of range"
    return get_quote(book_i, chapter_i, verse_i)


@plugin.listen(command='bible [book] [passage]')
def passage_command(bot, message: SteelyMessage, **kwargs):
    if 'passage' not in kwargs:
        book = random.randrange(len(bible))
        chapter = random.randrange(len(bible[book]["chapters"]))
        verse = random.randrange(len(bible[book]["chapters"][chapter]))
        bot.sendMessage(
                get_quote(book, chapter, verse),
                thread_id=message.thread_id, thread_type=message.thread_type)
    else:
        bot.sendMessage(
                get_quote_from_ref(kwargs['book'], kwargs['passage']),
                thread_id=message.thread_id, thread_type=message.thread_type)

