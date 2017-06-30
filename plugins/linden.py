from tinydb import TinyDB, Query
from tinydb.operations import increment


COMMAND = ".linden"
USERDB = TinyDB("../linden.json")
USER = Query()


def find_user_from_id(id, user_list):
    filtered = list(filter(lambda x: x['uid'] == id, user_list))
    return filtered[0] if len(list(filter(lambda x: x['uid'] == id, user_list))) > 0 else None

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    users_in_chat = bot.fetchAllUsers()

    if not message:
        search = USERDB.search(USER.fb_id == author_id)

        response = "bleugh"

        if len(search) != 0:
            response = "You have {0:d} lindens".format(search[0]["lindens"])
        else:
            # User does not exist - create user and send lindens

            user_name = find_user_from_id(author_id, users_in_chat)["name"]

            if user_name is None:
                response = "bad egg: user not found"
            else:
                USERDB.insert({
                    "fb_id": author_id,
                    "name": user_name,
                    "lindens": 0
                })

                response = "You have {0:d} lindens".format(0)

        bot.sendMessage(response, thread_id=thread_id, thread_type=thread_type)
        return
    else:
        message_split = message.split()

        sub_command = message_split[0]

        target = ' '.join(message_split[1:])

        try:
            if not sub_command:
                bot.sendMessage("bad egg: command not found", thread_id=thread_id, thread_type=thread_type)
                return

            if sub_command.lower() == 'give':
                search = USERDB.search(USER.name == target)

                response = "bleugh"

                if len(search) != 0 and find_user_from_id(author_id, users_in_chat) is not None:
                    if not find_user_from_id(author_id, users_in_chat)["name"] == target:
                        USERDB.update(increment('lindens'), USER.name == target)
                        search = USERDB.search(USER.name == target)
                        response = "{0:s} now has {1:d} lindens".format(target, search[0]["lindens"])
                    else:
                        response = "bad egg: you cannot give yourself lindens"
                else:
                    response = "bad egg: user not found"

                bot.sendMessage(response, thread_id=thread_id, thread_type=thread_type)
                return

        except ValueError:
            bot.sendMessage("bad egg: cannot parse amount", thread_id=thread_id, thread_type=thread_type)



if __name__ == "__main__":
    print("dello?")

    class bot:
        @staticmethod
        def sendMessage(*args, **kwargs):
            print("send", args, kwargs)
        @staticmethod
        def fetchAllUsers(*args, **kwargs):
            return([
                {"uid": "test", "name": "test"}
            ])

    # U N I T   T E S T I N G

    main(bot, "test", '', 1, 2)
    main(bot, "1", 'give test', 1, 2)
    main(bot, "1", 'give test', 1, 2)
    main(bot, "1", 'give test', 1, 2)
    main(bot, "1", 'give test', 1, 2)
    main(bot, "1", '', 1, 2)
