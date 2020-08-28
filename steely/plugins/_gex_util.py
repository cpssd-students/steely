import time
from tinydb import Query
from plugins import gex
from utils import new_database

USER_DB = new_database('gex_users')
USER = Query()
CARD_DB = new_database('gex_cards')
CARD = Query()

# Cache to map facebook IDs to real names.
ID_TO_NAME = {}


def user_name_to_id(bot, name):
    print('user_name_to_id(bot, {})'.format(name))
    users = bot.searchForUsers(name)
    print("Searched for", name, "got", users)
    return users['id']


def user_id_to_name(bot, user_id):
    if user_id in ID_TO_NAME:
        print('Cache hit for {} in user_id_to_name'.format(user_id))
        return ID_TO_NAME[user_id]
    try:
        users = bot.fetchUserInfo(user_id)
        if len(users) == 0:
            raise ValueError('No user found for ID {}'.format(user_id))
        ID_TO_NAME[user_id] = users[0]['full_name']
        return users[0]['full_name']
    except Exception as e:
        print('Error in user_id_to_name:')
        print(e)
        return 'Zucc'


def get_user(user_id):
    matching_users = USER_DB.search(USER.id == user_id)
    if not len(matching_users):
        raise RuntimeError('Could not find user with given id.')
    return matching_users[0]


def get_time_millis():
    millis = int(round(time.time() * 1000))
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
        'cards': {},
        'last_create_time': 0,
        'last_card': None,
    })

'''Get the attack power of a card.'''


def get_card_attack(card_id):
    card_to_user_id = gex.get_card_to_user_id()
    d = {card: sum(t[1] for t in card_to_user_id[card])
         for card in card_to_user_id}
    vals = sorted(d)
    vals = sorted(vals, key=lambda x: d[x])
    pos = vals.index(card_id) + 1
    return int(1000 * pos / len(vals))

'''Get the defence power of a card.'''


def get_card_defence(card_id):
    return 1000 - get_card_attack(card_id)
