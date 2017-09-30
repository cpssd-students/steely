from tinydb import TinyDB, Query

BATTLE_DB = TinyDB('databases/gex_battles.json')
BATTLE = Query()

def battle(bot, args, author_id, thread_id, thread_type):
    print('battle started')
