#!/usr/bin/env python3
'''
gex is a TCG-alike for the Followers of Nude Tayne.

See design doc at: https://docs.google.com/document/d/1HYDU3wrewmk9dwt6wX7MqMcbZfuaGSrfhP6YXsSORBY/edit?usp=sharing
'''

from tinydb import TinyDB, Query, where, operations

__author__ = 'iandioch'
COMMAND = '.gex'
CARD_DB = TinyDB('databases/gex_cards.json')
USER_DB = TinyDB('databases/gex_users.json')
CARD = Query()
USER = Query() # not sure if this is needed instead of reusing CARD but w/e

# Utility funcs

def _check_for_card(user, card_id):
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if not len(matching_cards):
        raise RuntimeError('No card exists with the given id.')
    if user not in matching_cards[0]['masters']:
        raise RuntimeError('User is not in masters of this card.')
    return matching_cards[0]

def _check_user_in_db(user_id):
    matching_users = USER_DB.search(USER.id == user_id)
    if len(matching_users):
        return
    USER_DB.insert({'id': user_id, 'cards':{}})

def _get_user(user_id):
    matching_users = USER_DB.search(USER.id == user_id)
    if not len(matching_users):
        raise RuntimeError('Could not find user with given id.')
    return matching_users[0]

def _user_name_to_id(bot, name):
    users = bot.searchForUsers(name)
    return users[0].uid

# Public API

'''
Give the specified receiver user the card with the given id.
'''
def gex_give(giving_user, card_id, receiving_user):
    print('giving', giving_user, card_id, receiving_user)
    _check_for_card(giving_user, card_id)
    _check_user_in_db(receiving_user)
    data = _get_user(receiving_user)
    cards = data['cards']
    if card_id in cards:
        cards[card_id] += 1
    else:
        cards[card_id] = 1
    USER_DB.update({'cards':cards}, USER.id == receiving_user)

'''
Remove the specified card from a certain user.
'''
def gex_remove(removing_user, card_id, receiving_user):
    print('removing', removing_user, card_id, receiving_user)
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if not len(matching_cards):
        raise RuntimeError('No card exists with the given id.')
    masters = matching_cards[0]['masters']
    if removing_user not in masters and removing_user != receiving_user:
        raise RuntimeError('Only a card master or the user themselves can remove a card.')
    _check_user_in_db(receiving_user)
    user = _get_user(receiving_user)
    if card_id not in user['cards'] or user['cards'][card_id] <= 0:
        raise RuntimeError('This user does not own the given card!')
    user['cards'][card_id] -= 1
    if user['cards'][card_id] == 0:
        del user['cards'][card_id]
    USER_DB.update({'cards':user['cards']}, USER.id == receiving_user)

'''
Set the image url for the card with the given id.
'''
def gex_set_image(user, card_id, card_image_url):
    _check_for_card(user, card_id)
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
    if len(card_id) > 16:
        raise RuntimeError('A card id may be no longer than 16 chars.')
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

'''
Get a list of all of the cards a user has, sorted by their occurances.
'''
def gex_flex(user_id):
    _check_user_in_db(user_id)
    data = _get_user(user_id)
    cards = data['cards']
    card_keys = list(cards)
    card_keys.sort()
    card_keys.sort(key = lambda x: cards[x], reverse=True)
    card_tuples = []
    for c in card_keys:
        card_tuples.append((c, cards[c]))
    return card_tuples

# Private message-based funcs

def _gex_give(bot, args, author_id, thread_id, thread_type):
    if not args or len(args) != 2:
        raise RuntimeError('Need to provide command in the form give USER CARD_ID .')
    user_id = _user_name_to_id(bot, args[0])
    # TODO(ndonn): Map from real name to user id.
    # TODO(ndonn): Respond if the given user does not exist in this channel.
    card_id = args[1]
    gex_give(author_id, card_id, user_id)
    # TODO(ndonn): Notify user they got a new card.

def _gex_remove(bot, args, author_id, thread_id, thread_type):
    if not args or len(args) != 2:
        raise RuntimeError('Need to provide command in the form remove USER CARD_ID .')
    user_id = _user_name_to_id(bot, args[0])
    # TODO(ndonn): Map from real name to user id.
    # TODO(ndonn): Respond if the given user does not exist in this channel.
    card_id = args[1]
    gex_remove(author_id, card_id, user_id)
    # TODO(ndonn): Notify user they lost a card.

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

def _gex_flex(bot, args, author_id, thread_id, thread_type):
    user_id = author_id
    if len(args):
        user_id = _user_name_to_id(bot, args[0])
    cards = gex_flex(user_id)
    total = sum(c[1] for c in cards)
    output = 'ID: {}\nCards:\n'.format(user_id)
    output += 'Total cards: {} ({} unique)\n'.format(total, len(cards))
    for card, num in cards:
        output += '{}: {}\n'.format(card, num)
    bot.sendMessage(output, thread_id=thread_id, thread_type=thread_type)


SUBCOMMANDS = {
    'give': _gex_give,
    'remove': _gex_remove,
    'set_image': _gex_set_image,
    'create': _gex_create,
    'inspect': _gex_inspect,
    'flex': _gex_flex,
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
