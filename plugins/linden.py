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


def give_cmd(bot, message_parts, author_id, thread_id, thread_type):
    users = list_users(bot, thread_id)
    if not message_parts[-1].isdigit() or message_parts[-1] == "0":
        bot.sendMessage('please enter a valid amount',
                        thread_id=thread_id, thread_type=thread_type)
        return
    reciever_name, amount = message_parts[0].lstrip("@").capitalize(), int(message_parts[-1])
    reciever_model = user_from_name(reciever_name, users)
    reciever = USERDB.get(USER.id == reciever_model.uid)
    sender_model = bot.fetchUserInfo(author_id)[author_id]
    sender = USERDB.get(USER.id == author_id)
    if sender_model.uid == reciever_model.uid:
        bot.sendMessage('no', thread_id=thread_id, thread_type=thread_type)
        return
    if not reciever:
        reciever = create_user(reciever_model.uid, reciever_model.first_name)
    if not sender:
        sender = create_user(author_id, sender_model.first_name)
    new_sender_balance = sender['lindens'] - amount
    if new_sender_balance < 0:
        bot.sendMessage('you\'d be broke boyo', thread_id=thread_id, thread_type=thread_type)
        return
    USERDB.update({'lindens': new_sender_balance}, USER.id == author_id)
    USERDB.update({'lindens': reciever['lindens'] + amount}, USER.id == reciever_model.uid)
    bot.sendMessage('you gave {} {} Linden Dollars™'.format(reciever_name, amount),
                    thread_id=thread_id, thread_type=thread_type)


def table_cmd(bot, message_parts, author_id, thread_id, thread_type):
    max_lindens = len(str(max(user['lindens'] for user in USERDB.all())))
    max_name = len(max((user['first_name'] for user in USERDB.all()), key=len))
    string = '```'
    for user in sorted(USERDB.all(), key=lambda user: user['lindens'], reverse=True):
        string += '\n{name:<{max_name}} {lindens:>{max_lindens}}L$'.format(name=user['first_name'],
                                                                         lindens=user['lindens'],
                                                                         max_name=max_name,
                                                                         max_lindens=max_lindens)
    string += '\n```'
    bot.sendMessage(string, thread_id=thread_id, thread_type=thread_type)


def invalid_cmd(bot, message_parts, author_id, thread_id, thread_type):
    bot.sendMessage("invalid subcommand", thread_id=thread_id, thread_type=thread_type)


SUBCOMMANDS = {
    'give': give_cmd,
    'send': give_cmd,
    'table': table_cmd,
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage('you have {} Linden Dollars™'.format(get_balance(author_id)),
                        thread_id=thread_id, thread_type=thread_type)
        return

    subcommand, *args = message.split()
    SUBCOMMANDS.setdefault(subcommand, invalid_cmd)(bot, args, author_id, thread_id, thread_type)


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
