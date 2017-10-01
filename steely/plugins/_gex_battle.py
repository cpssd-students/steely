import plugins._gex_util as gex_util
from tinydb import TinyDB, Query

BATTLE_DB = TinyDB('databases/gex_battles.json')
BATTLE = Query()

def _get_participant_info(bot, data):
    name = gex_util.user_id_to_name(bot, data['id'])
    deck = data['deck']
    return (name, deck)

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
    defender_id = gex_util.user_name_to_id(bot, defender_name)
    data = {
        'attacker': {
            'id': attacker_id,
            'deck': [],
        },
        'defender': {
            'id': defender_id,
            'deck': [],
        },
        'id': 'ohshit',
    }
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
