#!/usr/bin/env python3
'''
gex is a TCG-alike for the Followers of Nude Tayne.

See design doc at: https://docs.google.com/document/d/1HYDU3wrewmk9dwt6wX7MqMcbZfuaGSrfhP6YXsSORBY/edit?usp=sharing
'''

from tinydb import TinyDB, Query, where, operations

__author__ = 'iandioch'
COMMAND = '.gex'
CARD_DB = TinyDB('databases/gex_cards.json')
CARD = Query()

'''
Set the image url for the card with the given id.
'''
def gex_set_image(user, card_id, card_image_url):
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if not len(matching_cards):
        raise RuntimeError('No card exists with the given id.')
    if user not in matching_cards[0]['masters']:
        raise RuntimeError('User is not in masters of this card.')
    CARD_DB.update(operations.set('image', card_image_url), CARD.id == card_id)

'''
Create a gex card with the given id, masters list, and description.
'''
def gex_create(card_id, card_masters, card_desc=None):
    # TODO(iandioch): Put time-out in place, so a user must wait 24hrs before
    # they can create another gex card.
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

'''
Get information about the card with the given id.
'''
def gex_inspect(card_id):
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if not matching_cards:
        raise RuntimeError('No card exists with the given id.')
    return matching_cards[0]

# Private message-based funcs

def _gex_set_image(bot, args, author_id, thread_id, thread_type):
    if not args or len(args) == 1:
        raise RuntimeError('Need to provide command in the form set_image ID URL .')
    card_id = args[0]
    card_image = ' '.join(args[1:])
    gex_set_image(author_id, card_id, card_image)
    bot.sendMessage('Image successfully set to {}'.format(card_image), thread_id=thread_id, thread_type=thread_type)
    bot.sendRemoteImage(card_image, thread_id=thread_id, thread_type=thread_type)

def _gex_create(bot, args, author_id, thread_id, thread_type):
    # gex create id desc
    if not args:
        raise RuntimeError('Need to provide command in the form create ID [DESC] .')
        return
    card_id = args[0]
    card_desc = None
    if len(args) > 1:
        card_desc = ' '.join(args[1:])
    gex_create(card_id, [author_id], card_desc)
    bot.sendMessage('Card {} created.'.format(card_id), thread_id=thread_id, thread_type=thread_type)

def _gex_inspect(bot, args, author_id, thread_id, thread_type):
    if not args:
        raise RuntimeError('Need to provide a card id.')
    deets = gex_inspect(args[0])
    print(deets)
    if deets['image'] and deets['image'] is not None:
        print('inspecting image', deets['image'])
        bot.sendRemoteImage(deets['image'], thread_id=thread_id, thread_type=thread_type)
    info = '*{}*\n'.format(deets['id'])
    if deets['desc'] is not None:
        info += '_{}_\n\n'.format(deets['desc'])
    # TODO(iandioch): Get user names instead of ID number of masters.
    info += 'Masters: ' + ', '.join(deets['masters'])
    bot.sendMessage(info, thread_id=thread_id, thread_type=thread_type)

SUBCOMMANDS = {
    'set_image': _gex_set_image,
    'create': _gex_create,
    'inspect': _gex_inspect,
}

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        # User just typed .gex
        commands = 'Please use one of the following gex commands, for a low low fee of 5 euroboys:\n' + \
                '\n'.join(SUBCOMMANDS.keys().sort())
        bot.sendMessage(commands, thread_id=thread_id, thread_type=thread_type)
        return
    subcommand, *args = message.split()
    if subcommand in SUBCOMMANDS:
        try:
            SUBCOMMANDS[subcommand](bot, args, author_id, thread_id, thread_type)
        except RuntimeError as e:
            bot.sendMessage('Error while gexin\': {}'.format(e), thread_id=thread_id, thread_type=thread_type)
        except Exception as e:
            bot.sendMessage('Misc error: {}'.format(e), thread_id=thread_id, thread_type=thread_type)
        return

    bot.sendMessage('Could not find command {}! Gex better son.'.format(subcommand), thread_id=thread_id, thread_type=thread_type)

    # no such subcommand found
