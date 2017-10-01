from random import shuffle
import uuid
from tinydb import TinyDB, Query
from fbchat.models import ThreadType
import plugins._gex_util as gex_util

BATTLE_DB = TinyDB('databases/gex_battles.json')
BATTLE = Query()

# The number of cards coming up in the deck that users can see.
NUM_UPCOMING_CARDS_TO_DISPLAY = 5
# The amount of power each user starts with in a battle.
STARTING_POWER_AMOUNT = 50

def _get_participant_info(bot, data):
    name = gex_util.user_id_to_name(bot, data['id'])
    deck = data['deck']
    ready = data['ready']
    power = data['power']
    return (name, deck, ready, power)

'''Get a permutation of a user's cards.'''
def _get_shuffled_deck(user_id):
    user_data = gex_util.get_user(user_id)
    cards = []
    for card in user_data['cards']:
        cards.extend([card]*(user_data['cards'][card]))
    shuffle(cards)
    return cards

def _generate_battle_id():
    while True:
        _id = uuid.uuid4().hex[:4]
        matching_battles = BATTLE_DB.search(BATTLE.id == _id)
        if len(matching_battles) > 0:
            continue
        print('Started battle with id {}'.format(_id))
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
    out = '*Battle {}*'.format(battle_id)
    out += '\nAttacker: {}\n{} ⚡\nDeck:'.format(attacker_info[0], attacker_info[3])
    for i in range(min(NUM_UPCOMING_CARDS_TO_DISPLAY, len(attacker_info[1]))):
        out  += '\n`{}` ({})'.format(attacker_info[1][i], 1) # TODO: replace with card power
    if attacker_info[2]:
        out += '\n_Ready to fight._'
    else:
        out += '\n_Not ready._'
    defender_info = _get_participant_info(bot, defender)
    out += '\n\nDefender: {}\n{} ⚡\nDeck:'.format(defender_info[0], defender_info[3])
    for i in range(min(NUM_UPCOMING_CARDS_TO_DISPLAY, len(defender_info[1]))):
        out  += '\n`{}` ({})'.format(defender_info[1][i], 1) # TODO: replace with card power
    if defender_info[2]:
        out += '\n_Ready to fight._'
    else:
        out += '\n_Not ready._'
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)

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
    battle_id = _generate_battle_id()
    data = {
        'attacker': {
            'id': attacker_id,
            'deck': _get_shuffled_deck(attacker_id),
            'ready': False,
            'power': STARTING_POWER_AMOUNT,
        },
        'defender': {
            'id': defender_id,
            'deck': _get_shuffled_deck(defender_id),
            'ready': False,
            'power': STARTING_POWER_AMOUNT,
        },
        'id': battle_id,
        'thread_id': thread_id,
        'is_group_thread': (thread_type == ThreadType.GROUP),
    }
    print(data)
    BATTLE_DB.insert(data)
    bot.sendMessage('Started battle {}.'.format(battle_id), thread_id=thread_id, thread_type=thread_type)

def battle_ready(bot, args, author_id, thread_id, thread_type):
    if len(args) == 0:
        bot.sendMessage('Please provide a battle ID.', thread_id=thread_id, thread_type=thread_type)
        return
    battle_id = args[0]
    matching_battles = BATTLE_DB.search(BATTLE.id == battle_id)
    if len(matching_battles) == 0:
        bot.sendMessage('No battle found with given ID.', thread_id=thread_id, thread_type=thread_type)
        return
    battle = matching_battles[0]
    if author_id == battle['attacker']['id']:
        battle['attacker']['ready'] = True
    elif author_id == battle['defender']['id']:
        battle['defender']['ready'] = True
    else:
        bot.sendMessage('This user is not a part of this battle.', thread_id=thread_id, thread_type=thread_type)
        return
    BATTLE_DB.update(battle, BATTLE.id == battle_id)

subcommands = {
    'info': battle_info,
    'start': battle_start,
    'ready': battle_ready,
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
