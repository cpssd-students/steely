import time
from tinydb import TinyDB, Query

USER_DB = TinyDB('databases/gex_users.json')
USER = Query()
CARD_DB = TinyDB('databases/gex_cards.json')
CARD = Query()

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

def get_user(user_id):
    matching_users = USER_DB.search(USER.id == user_id)
    if not len(matching_users):
        raise RuntimeError('Could not find user with given id.')
    return matching_users[0]

def get_time_millis():
    millis = int(round(time.time()*1000))
    return millis

def check_for_card(user, card_id):
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if not len(matching_cards):
        raise RuntimeError('No card exists with the given id.')
    if user not in matching_cards[0]['masters']:
        raise RuntimeError('User is not in masters of this card.')
    return matching_cards[0]

def check_user_in_db(user_id):
    matching_users = USER_DB.search(USER.id == user_id)
    if len(matching_users):
        return
    time_millis = get_time_millis()
    USER_DB.insert({
        'id': user_id,
        'cards':{},
        'last_create_time': 0,
        'last_card': None,
    })

'''Get the power of this card in a battle'''
def get_card_value(card_id):
    return len(card_id)
