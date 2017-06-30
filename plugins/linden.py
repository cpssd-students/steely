import random


COMMAND = '.give'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    return

    # how the shit do you get the nick of a user in fbchat

    # if len(message.split()) != 2:
    #     bot.sendMessage("must be like '.give <user> <amount>'", thread_id=thread_id, thread_type=thread_type)
    #     return
    split_message = message.split()
    user, amount = ' '.join(split_message[:-1]), split_message[-1]


    # sender = bot.fetchUserInfo(author_id)[author_id]
    # print(sender.own_nickname)
    # print(sender.nickname)
    # print(sender.type)
    # print(sender.url)
    # print(sender.first_name)
    # print(sender.last_name)

    # reciever_user_id = bot.searchForUsers(user.replace('@', ''))[0]
    # reciever = bot.fetchUserInfo(reciever_user_id).keys()[reciever_user_id]
    # print(reciever.own_nickname)
    # print(reciever.nickname)
    # print(reciever.type)
    # print(reciever.url)
    # print(reciever.first_name)
    # print(reciever.last_name)
