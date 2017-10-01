from random import shuffle
import uuid
from tinydb import TinyDB, Query
import plugins._gex_util as gex_util

BATTLE_DB = TinyDB('databases/gex_battles.json')
BATTLE = Query()

def _get_participant_info(bot, data):
    name = gex_util.user_id_to_name(bot, data['id'])
    deck = data['deck']
    return (name, deck)

'''Get a permutation of a user's cards.'''
def _get_shuffled_deck(user_id):
    user_data = gex_util.get_user(user_id)
    cards = []
    for card in user_data['cards']:
        cards.extend([card]*(user_data['cards'][card]))
    shuffle(cards)
    return cards

def _generate_battle_id():
    _id = uuid.uuid4().hex[:4]
    print(_id)
    return _id

def battle_info(bot, args, author_id, thread_id, thread_type):
    if len(args) == 0:
        bot.sendMessage('Please provide a battle ID!', thread_id=thread_id, thread_type=thread_type)
        return
    battle_id = args[0]
    matching_battles = BATTLE_DB.search(BATTLE.id == battle_id)
    if len(matching_battles) == 0:
        bot.sendMessage('No battle found with the given ID :(', thread_id=thread_id, thread_type=thread_type)
        return
    battle = matching_battles[0]
    attacker = battle['attacker']
    defender = battle['defender']
    attacker_info = _get_participant_info(bot, attacker)
    print(attacker_info)
    bot.sendMessage(str(attacker_info), thread_id=thread_id, thread_type=thread_type)

def battle_start(bot, args, author_id, thread_id, thread_type):
    attacker_id = author_id
    if len(args) == 0:
        bot.sendMessage('Please choose someone to battle xo', thread_id=thread_id, thread_type=thread_type)
        return
    defender_name = args[0]
    print(defender_name)
    defender_id = gex_util.user_name_to_id(bot, defender_name)
    gex_util.check_user_in_db(attacker_id)
    gex_util.check_user_in_db(defender_id)
    print(defender_id)
    data = {
        'attacker': {
            'id': attacker_id,
            'deck': _get_shuffled_deck(attacker_id),
        },
        'defender': {
            'id': defender_id,
            'deck': _get_shuffled_deck(defender_id),
        },
        'id': _generate_battle_id(),
    }
    print(data)
    BATTLE_DB.insert(data)

subcommands = {
    'info': battle_info,
    'start': battle_start,
}

def battle(bot, args, author_id, thread_id, thread_type):
    # Should be in format .gex battle <subcommand>.
    if len(args) == 0:
        bot.sendMessage('Should be run in form .gex battle SUBCOMMAND .', thread_id=thread_id, thread_type=thread_type)
        return
    subcommand = args[0]
    if subcommand in subcommands:
        try:
            subcommands[subcommand](bot, args[1:], author_id, thread_id, thread_type)
        except Exception as e:
            bot.sendMessage('Battle error: {}'.format(e), thread_id=thread_id, thread_type=thread_type)
    else:
        bot.sendMessage('No such subcommand >:(', thread_id=thread_id, thread_type=thread_type)
