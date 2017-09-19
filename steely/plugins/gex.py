#!/usr/bin/env python3
'''
gex is a TCG-alike for the Followers of Nude Tayne.

See design doc at: https://docs.google.com/document/d/1HYDU3wrewmk9dwt6wX7MqMcbZfuaGSrfhP6YXsSORBY/edit?usp=sharing
'''

from tinydb import TinyDB, Query, where

__author__ = 'iandioch'
COMMAND = '.gex'
CARD_DB = TinyDB('databases/gex_cards.json')
CARD = Query()

'''
Create a gex card with the given id, masters set, and description
'''
def gex_create_card(card_id, card_masters, card_desc=None):
    if not card_masters or not len(card_masters):
        raise RuntimeError('No master provided for this card.')
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if len(matching_cards):
        raise RuntimeError('A card already exists with this id.')
    CARD_DB.insert({
        'id': card_id,
        'masters': card_masters,
        'desc': card_desc,
        'image': None,
    })

def _gex_create(bot, args, author_id, thread_id, thread_type):
    # gex create id desc
    if not args:
        # incorrect syntax
        return
    card_id = args[0]
    card_desc = None
    if len(args) > 1:
        card_desc = ' '.join(args[1:])
    gex_create_card(card_id, set(author_id), card_desc)

SUBCOMMANDS = {
    'create': _gex_create,
}

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        # User just typed .gex
        return
    subcommand, *args = message.split()
    if subcommand in SUBCOMMANDS:
        SUBCOMMANDS[subcommand](bot, args, author_id, thread_id, thread_type)
        return

    # no such subcommand found
