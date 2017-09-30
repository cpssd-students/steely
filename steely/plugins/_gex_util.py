from tinydb import TinyDB, Query

USER_DB = TinyDB('databases/gex_users.json')
User = Query()

def get_user(user_id):
    matching_users = USER_DB.search(USER.id == user_id)
    if not len(matching_users):
        raise RuntimeError('Could not find user with given id.')
    return matching_users[0]

def user_name_to_id(bot, name):
    users = bot.searchForUsers(name)
    return users[0].uid

def user_id_to_name(bot, user_id):
    user = bot.fetchUserInfo(user_id)[user_id]
    return user.name
