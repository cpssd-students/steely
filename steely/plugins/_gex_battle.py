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

BATTLE_COMMANDS = {
    '!SWAP': 5,
}

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

def _perform_battle_round(bot, battle_id):
    matching_battles = BATTLE_DB.search(BATTLE.id == battle_id)
    if len(matching_battles) == 0:
        raise RuntimeError('No such battle id to perform round in!')
    battle = matching_battles[0]
    keys = ('attacker', 'defender')
    for key in keys:
        if 'commands' not in battle[key]:
            continue
        commands = battle[key]['commands']
        # Do not assume all commands are valid.
        for command in commands:
            if command == '!SWAP':
                if len(battle[key][deck]) < 2:
                    raise RuntimeError('User did not have enough cards to swap!')
                elif battle[key]['power'] < BATTLE_COMMANDS['!SWAP']:
                    raise RuntimeError('User did not have enough ⚡ to swap!')
                battle[key][deck][0], battle[key][deck][1] = battle[key][deck][1], battle[key][deck][0]
    attacker_card = battle['attacker']['deck'].pop(0)
    defender_card = battle['defender']['deck'].pop(0)
    
    def lost_round(key):
        battle[key]['power'] -= 10
        print(key, 'lost')

    if gex_util.get_card_value(attacker_card) >= gex_util.get_card_value(defender_card):
        lost_round('defender')
    else:
        lost_round('attacker')
    battle['attacker']['ready'] = False
    battle['defender']['ready'] = False
    BATTLE_DB.update(battle, BATTLE.id == battle_id)

def _check_for_battle_finish(bot, battle_id):
    matching_battles = BATTLE_DB.search(BATTLE.id == battle_id)
    battle = matching_battles[0]
    winner, loser = None, None
    if battle['attacker']['power'] <= 0 or len(battle['attacker']['deck']) == 0:
        # attacker lost
        winner = battle['defender']['id']
        loser = battle['attacker']['id']
    elif battle['defender']['power'] <= 0 or len(battle['defender']['deck']) == 0:
        # defender lost
        winner = battle['attacker']['id']
        loser = battle['defender']['id']
    else:
        return
    winner_name = gex_util.user_id_to_name(bot, winner)
    loser_name = gex_util.user_id_to_name(bot, loser)
    thread_id = battle['thread_id']
    thread_type = ThreadType.GROUP if battle['is_group_thread'] else ThreadType.USER
    out = '_{}_ won battle `{}` against _{}_'.format(winner_name, battle_id, loser_name)
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)

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
        out  += '\n`{}` ({})'.format(attacker_info[1][i], gex_util.get_card_value(attacker_info[1][i]))
    if attacker_info[2]:
        out += '\n_Ready to fight._'
    else:
        out += '\n_Not ready._'
    defender_info = _get_participant_info(bot, defender)
    out += '\n\nDefender: {}\n{} ⚡\nDeck:'.format(defender_info[0], defender_info[3])
    for i in range(min(NUM_UPCOMING_CARDS_TO_DISPLAY, len(defender_info[1]))):
        out  += '\n`{}` ({})'.format(defender_info[1][i], gex_util.get_card_value(defender_info[1][i]))
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
            'commands': [],
        },
        'defender': {
            'id': defender_id,
            'deck': _get_shuffled_deck(defender_id),
            'ready': False,
            'power': STARTING_POWER_AMOUNT,
            'commands': [],
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
    if (battle['attacker']['ready'] and battle['defender']['ready']):
        _perform_battle_round(bot, battle_id)
        _check_for_battle_finish(bot, battle_id)

def battle_list(bot, args, author_id, thread_id, thread_type):
    user_id = author_id
    if len(args) != 0:
        user_id = gex_util.user_name_to_id(bot, ' '.join(args))
    user_name = gex_util.user_id_to_name(bot, user_id)

    out = ''
    matching_battles = BATTLE_DB.search(BATTLE.defender.id == user_id)
    if len(matching_battles) > 0:
        out = 'Battles in which {} is defending:'.format(user_name)
        for battle in matching_battles:
            opponent_id = battle['attacker']['id']
            opponent_name = gex_util.user_id_to_name(bot, opponent_id)
            out += '\n' + '`{}` (against _{}_)'.format(battle['id'], opponent_name)
    matching_battles = BATTLE_DB.search(BATTLE.attacker.id == user_id)
    if len(matching_battles) > 0:
        out += '\nBattles in which {} is attacking:'.format(user_name)
        for battle in matching_battles:
            opponent_id = battle['defender']['id']
            opponent_name = gex_util.user_id_to_name(bot, opponent_id)
            out += '\n' + '`{}` (against _{}_)'.format(battle['id'], opponent_name)
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)


subcommands = {
    'info': battle_info,
    'start': battle_start,
    'ready': battle_ready,
    'list': battle_list,
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
