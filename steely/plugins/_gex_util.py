from tinydb import TinyDB, Query

# Cache to map facebook IDs to real names.
ID_TO_NAME = {}

def user_name_to_id(bot, name):
    users = bot.searchForUsers(name)
    return users[0].uid

def user_id_to_name(bot, user_id):
    if user_id in ID_TO_NAME:
        return ID_TO_NAME[user_id]
    try:
        user = bot.fetchUserInfo(user_id)[user_id]
        ID_TO_NAME[user_id] = user.name
        return user.name
    except Exception:
        return 'Zucc'
