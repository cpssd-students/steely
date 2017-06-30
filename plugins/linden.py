#!/usr/bin/env python3


from tinydb import TinyDB, Query, where
from tinydb.operations import increment


COMMAND = ".linden"
USERDB = TinyDB("../linden.json")
USER = Query()


def user_from_id(id, list):
    for user in list:
        if user['uid'] == id:
            return user


def user_from_name(name, list):
    for user in list:
        if user['name'] == name:
            return user


def create_user(user):
    USERDB.insert({
        "uid": user['uid'],
        "name": user['name'],
        "lindens": 2000
    })


def get_balance(user_id):
    matching_users = USERDB.search(USER.uid == user_id)
    if len(matching_users) == 0:
        return
    return matching_users['lindens']


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage('you have {} Linden Dollars™'.format(get_balance(author_id),
            thread_id=thread_id, thread_type=thread_type))
        return

    message_split = message.split()
    users = bot.fetchAllUsers()
    if message_split[0] in ('give', 'send') and len(message_split) > 2:
        if not message_split[-1].isdigit():
            bot.sendMessage('please enter a valid amount', thread_id=thread_id, thread_type=thread_type)
            return
        reciever_name, amount = ' '.join(message_split[1:-1]), int(message_split[-1])
        if not USERDB.search(where('name') == reciever_name):
            create_user(user_from_name(reciever_name, users))
        if not USERDB.search(where('uid') == author_id):
            create_user(user_from_id(author_id, users))
        reciever = USERDB.get(USER.name == reciever_name)
        sender = USERDB.get(USER.uid == author_id)
        USERDB.update({'lindens': reciever['lindens'] + amount}, USER.name == reciever_name)
        USERDB.update({'lindens': sender['lindens'] - amount}, USER.uid == author_id)
        bot.sendMessage('you gave {} {} Linden Dollars™'.format(reciever_name, amount),
            thread_id=thread_id, thread_type=thread_type)
        return

    if message_split[0] == 'table' and len(message_split) == 1:
        max_lindens = len(str(max(user['lindens'] for user in USERDB.all())))
        max_name = len(max((user['name'] for user in USERDB.all()), key=len))
        string = '```\n'
        for user in sorted(USERDB.all(), key=lambda user: user['lindens'], reverse=True):
            string += '{name:<{max_name}} {lindens:>{max_lindens}}\n'.format(name=user['name'],
                                                                             lindens=user['lindens'],
                                                                             max_name=max_name,
                                                                             max_lindens=max_lindens)
            string += '```'
        bot.sendMessage(string, thread_id=thread_id, thread_type=thread_type)))
    USERDB.close()


if __name__ == "__main__":
    # tests
    class Bot:

        @staticmethod
        def sendMessage(message, *args, **kwargs):
            print(message)

        @staticmethod
        def fetchAllUsers(*args, **kwargs):
            return [{"uid": "2343", "name": "steely"},
                    {"uid": "5435", "name": "dan"},
                    {"uid": "54344445", "name": "egg gggggggbobu"}]

    b = Bot()
    main(Bot, '2343', 'send dan 6', 1, 1)
    main(Bot, '2343', 'send egg gggggggbobu 6', 1, 1)
    main(Bot, '2343', 'table', 1, 1)
