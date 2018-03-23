#!/usr/bin/env python3

'''
.bug <bug title> - <bug descripsion>
.bug info <bug title>
.bug list

bug titles can't be longer than 20 chars
bug descriptions can't be longer than 1000 chars or less than 20 chars.
'''

from tinydb import TinyDB, Query
import formatting

__author__ = 'devoxel'
COMMAND = 'bug'

# TODO: add descriptive error messages
ERR_MSG = "i'm sorry sam.. i'm afraid I can't do that."

BUG_DB = TinyDB('databases/bug.json')
Bug = Query()

def get_bug_info(m):
    if len(m) != 2:
        return ERR_MSG

    # first try by id
    try:
        s = BUG_DB.get(doc_id=int(m[1]))
    except ValueError:
        s = BUG_DB.get(Bug.title == m[1])

    if s is None:
        return "no bug found"

    return f'#{s.doc_id}: {s["title"]}\n{s["desc"]}'

def list_bugs(_):
    o = []
    for item in BUG_DB:
        o.append(f'{item.doc_id}:\t{item["title"]}')
    return formatting.code_block('\n'.join(o))

def add_bug(m):
    if len(m) < 2:
        return ERR_MSG

    title, desc = m[0], m[1]
    if len(title) > 15 or len(desc) > 1000 or len(desc) < 20:
        return ERR_MSG

    BUG_DB.insert({
        'title': m[0],
        'desc': m[1],
    })
    return 'bug added'

COMMANDS = {
        'list': list_bugs,
        'info': get_bug_info,
}

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    m = message.split(maxsplit=1)
    cmd = m[0]
    if cmd in COMMANDS:
        r = COMMANDS[cmd](m[1:])
    else:
        r = add_bug(m.split('-'))

    bot.sendMessage(r, thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
    s = add_bug(["2", "22bad bug >:("])
    print(s)
    s = list_bugs("isjdojfo")
    print(s)
    s = get_bug_info("info good bug".split(maxsplit=1))
    print(s)
    s = get_bug_info("info 2".split(maxsplit=1))
    print(s)
