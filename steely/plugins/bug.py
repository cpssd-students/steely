#!/usr/bin/env python3

'''
.bug <bug title>
.bug comment <id> <comment>
.bug info <bug title>
.bug list

bug titles can't be longer than 45 chars

TODO: Add bug delete, bug modify, bug close and bug comment
'''

from tinydb import TinyDB, Query
import formatting

__author__ = 'devoxel'
COMMAND = 'bug'

# TODO: add descriptive error messages
ERR_MSG = "i'm sorry sam.. i'm afraid I can't do that."

BUG_DB = TinyDB('databases/bug.json')
Bug = Query()

def get_bug(search):
    # first try by id
    try:
        s = BUG_DB.get(doc_id=int(search))
    except ValueError:
        s = BUG_DB.get(Bug.title == search)
    return s

def get_bug_info(m):
    m = m.split(maxsplit=1)
    if len(m) != 2:
        return ERR_MSG

    s = get_bug(m[1])
    if s is None:
        return "no bug found"

    comments = "no comments"
    if len(s["comments"]) > 0:
        comments = '\n'.join(s["comments"])

    return f'#{s.doc_id}: {s["title"]}\n{comments}'

def list_bugs(_):
    o = [ f'{item.doc_id}:  {item["title"]}' for item in BUG_DB]
    return formatting.code_block('\n'.join(o))

def unsanitary(t):
    bad_chars = '`\n'
    return any(e in bad_chars for e in t)

def add_bug(title):
    if len(title) > 45 or unsanitary(title):
        return ERR_MSG

    a = BUG_DB.insert({
        'title': title,
        'comments': [],
    })
    return 'added bug {}'.format(a)

def comment_on_bug(m):
    m = m.split(maxsplit=2)
    if len(m) < 3:
        return ERR_MSG
    b = get_bug(m[1])
    if b is None:
        return ERR_MSG
    if unsanitary(m[2]):
        return ERR_MSG

    b['comments'].append(m[2])
    BUG_DB.update({'comments': b['comments']}, doc_ids=[b.doc_id])
    return "cool"

COMMANDS = {
        'list': list_bugs,
        'info': get_bug_info,
        'comment': comment_on_bug,
}

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    m = message.split(maxsplit=1)
    cmd = m[0]
    if cmd in COMMANDS:
        r = COMMANDS[cmd](message)
    else:
        r = add_bug(message)

    bot.sendMessage(r, thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
    s = add_bug("add ting")
    print(s)
    s = add_bug("add ``` ting ```")
    print(s)
    s = list_bugs("isjdojfo")
    print(s)
    s = get_bug_info("info good bug")
    print(s)
    s = comment_on_bug("comment 2 this one \n is gonna be hard")
    print(s)
    s = get_bug_info("info 2")
    print(s)
