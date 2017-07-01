#!/usr/bin/env python3


from tinydb import TinyDB, Query, where
from tinydb.operations import increment


COMMAND = ".linden"
USERDB = TinyDB("linden.json")
USER = Query()


def user_from_name(name, list):
    for user in list:
        if user.first_name == name:
            return user

def list_users(bot, thread_id):
    group = bot.fetchGroupInfo(thread_id)[thread_id]
    user_ids = group.participants
    yield from bot.fetchUserInfo(*user_ids).values()


def create_user(id, first_name):
    data = {"id": id,
            "first_name": first_name,
            "lindens": 2000}
    USERDB.insert(data)
    return data


def get_balance(user_id):
    matching_users = USERDB.get(USER.id == user_id)
    if len(matching_users) == 0:
        return
    return matching_users['lindens']


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    # .linden
    if not message:
        bot.sendMessage('you have {} Linden Dollars™'.format(get_balance(author_id)),
            thread_id=thread_id, thread_type=thread_type)
        return

    # .linden give <user> <amt>
    message_split = message.split()
    users = list_users(bot, thread_id)
    if message_split[0] in ('give', 'send') and len(message_split) > 2:
        if not message_split[-1].isdigit():
            bot.sendMessage('please enter a valid amount', thread_id=thread_id, thread_type=thread_type)
            return
        reciever_name, amount = message_split[1].lstrip("@"), int(message_split[-1])
        reciever_model = user_from_name(reciever_name, users)
        reciever = USERDB.get(USER.id == reciever_model.uid)
        sender_model = bot.fetchUserInfo(author_id)[author_id]
        sender = USERDB.get(USER.id == author_id)
        if not reciever:
            reciever = create_user(reciever_model.uid, reciever_model.first_name)
        if not sender:
            sender = create_user(author_id, sender_model.first_name)
        USERDB.update({'lindens': reciever['lindens'] + amount}, USER.id == reciever_model.uid)
        USERDB.update({'lindens': sender['lindens'] - amount}, USER.id == author_id)
        bot.sendMessage('you gave {} {} Linden Dollars™'.format(reciever_name, amount),
            thread_id=thread_id, thread_type=thread_type)
        return

    # .linden table
    if message_split[0] in ('table', 'list', 'stats') and len(message_split) == 1:
        max_lindens = len(str(max(user['lindens'] for user in USERDB.all())))
        max_name = len(max((user['first_name'] for user in USERDB.all()), key=len))
        string = '```'
        for user in sorted(USERDB.all(), key=lambda user: user['lindens'], reverse=True):
            string += '\n{name:<{max_name}} {lindens:>{max_lindens}}'.format(name=user['first_name'],
                                                                             lindens=user['lindens'],
                                                                             max_name=max_name,
                                                                             max_lindens=max_lindens)
        string += '\n```'
        bot.sendMessage(string, thread_id=thread_id, thread_type=thread_type)


if __name__ == "__main__":
    # tests
    class Bot:

        @staticmethod
        def sendMessage(message, *args, **kwargs):
            print(message)

        @staticmethod
        def fetchAllUsers(*args, **kwargs):
            return [{"id": "2343", "name": "steely"},
                    {"id": "5435", "name": "dan"},
                    {"id": "54344445", "name": "egg gggggggbobu"}]

    b = Bot()
    main(Bot, '2343', 'send dan 6', 1, 1)
    main(Bot, '2343', 'send egg gggggggbobu 6', 1, 1)
    main(Bot, '2343', 'table', 1, 1)
