#!/usr/bin/env python3

'''
.bug <bug title>
.bug comment <id> <comment>
.bug info <bug title>
.bug list

bug titles can't be longer than 45 chars

TODO: Add bug delete, bug modify, bug close and bug comment
'''

from tinydb import Query
import formatting
from utils import new_database

__author__ = 'devoxel'
COMMAND = 'bug'
ERR_MSG = "i'm sorry sam.. i'm afraid I can't do that."
BUG_DB = new_database('bug')
Bug = Query()

def get_bug(search):
    # first try by id
    try:
        s = BUG_DB.get(doc_id=int(search))
    except ValueError:
        s = BUG_DB.get(Bug.title == search)
    return s

def get_bug_info(command):
    command = command.split(maxsplit=1)
    if len(command) != 2:
        return ERR_MSG

    bug = get_bug(command[1])
    if bug is None:
        return "no bug found"

    comments = "no comments"
    if len(bug["comments"]) > 0:
        comments = '\n'.join(bug["comments"])

    return f'#{bug.doc_id}: {bug["title"]}\n{comments}'

def list_bugs(_):
    bugs = [ f'{bug.doc_id}:  {bug["title"]}' for bug in BUG_DB]
    return formatting.code_block('\n'.join(bugs))

def unsanitary(message):
    bad_chars = '`\n'
    return any(char in bad_chars for char in message)

def add_bug(title):
    if len(title) > 45 or unsanitary(title):
        return ERR_MSG

    id = BUG_DB.insert({
        'title': title,
        'comments': [],
    })
    return 'added bug {}'.format(id)

def comment_on_bug(command):
    command = command.split(maxsplit=2)
    if len(command) < 3:
        return ERR_MSG
    bug = get_bug(command[1])
    if bug is None:
        return ERR_MSG
    if unsanitary(command[2]):
        return ERR_MSG

    bug['comments'].append(command[2])
    BUG_DB.update({'comments': bug['comments']}, doc_ids=[bug.doc_id])
    return "cool"

COMMANDS = {
        'list': list_bugs,
        'info': get_bug_info,
        'comment': comment_on_bug,
}

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    command = message.split(maxsplit=1)
    cmd = command[0]
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
