#!/usr/bin/env python3
'''
gex is a TCG-alike for the Followers of Nude Tayne.

See design doc at: https://docs.google.com/document/d/1HYDU3wrewmk9dwt6wX7MqMcbZfuaGSrfhP6YXsSORBY/edit?usp=sharing
'''

import time
import heapq
import difflib
from tinydb import Query, where, operations
import plugins._gex_util as gex_util
from plugins import _gex_battle
from formatting import *

__author__ = 'iandioch'
COMMAND = 'gex'
CARD_DB = gex_util.CARD_DB
USER_DB = gex_util.USER_DB
CARD = gex_util.CARD
USER = gex_util.USER

# IDs that don't need auth to create cards (ie. Reed)
GOD_IDS = set(['100018746416184', '100022169435132', '100003244958231'])
# A dict mapping card_id to a list of tuples, where each is of the form:
# (user_id, quantity)
# This is a map of how many of a card each person with that card possesses.
# This dict is not kept in a DB, but is recalculated on each server init.
# This makes consistency with USER_DB's data much easier.
CARD_TO_USER_ID = {}
# Maximum length for a card id.
MAX_CARD_ID_LENGTH = 16
# Scrabble scores for each letter.
SCRABBLE_SCORES = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
                   "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, "x": 8, "z": 10}

# Utility funcs


def _load_card_to_user_id():
    global CARD_TO_USER_ID
    CARD_TO_USER_ID = {}
    users = USER_DB.all()
    for user in users:
        user_id = user['id']
        cards = user['cards']
        for card_id in cards:
            if card_id in CARD_TO_USER_ID:
                CARD_TO_USER_ID[card_id].append((user_id, cards[card_id]))
            else:
                CARD_TO_USER_ID[card_id] = [(user_id, cards[card_id])]


def _get_scrabble_score(s):
    ans = 0
    for c in s.lower():
        if not c.isalpha():
            continue
        if c in SCRABBLE_SCORES:
            ans += SCRABBLE_SCORES[c]
        else:
            ans += 2
    return ans

# Public API


def get_card_to_user_id():
    return CARD_TO_USER_ID

'''
Give the specified receiver user the card with the given id.
'''


def gex_give(giving_user, card_id, receiving_user):
    global CARD_TO_USER_ID
    print('giving', giving_user, card_id, receiving_user)
    gex_util.check_for_card(giving_user, card_id)
    gex_util.check_user_in_db(receiving_user)
    data = gex_util.get_user(receiving_user)
    cards = data['cards']
    if card_id in cards:
        cards[card_id] += 1
    else:
        cards[card_id] = 1
    USER_DB.update({'cards': cards, 'last_card': card_id},
                   USER.id == receiving_user)

    # Update CARD_TO_USER_ID
    tups = []
    if card_id in CARD_TO_USER_ID:
        tups = CARD_TO_USER_ID[card_id]
    indexes = [i for i in range(len(tups)) if tups[i][0] == receiving_user]
    if len(indexes):
        tups[indexes[0]] = (receiving_user, cards[card_id])
    else:
        tups.append((receiving_user, cards[card_id]))
    CARD_TO_USER_ID[card_id] = tups

'''
Remove the specified card from a certain user.
'''


def gex_remove(removing_user, card_id, receiving_user):
    global CARD_TO_USER_ID
    print('removing', removing_user, card_id, receiving_user)
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if not len(matching_cards):
        raise RuntimeError('No card exists with the given id.')
    masters = matching_cards[0]['masters']
    if removing_user not in masters and removing_user != receiving_user:
        raise RuntimeError(
            'Only a card master or the user themselves can remove a card.')
    gex_util.check_user_in_db(receiving_user)
    user = gex_util.get_user(receiving_user)
    if card_id not in user['cards'] or user['cards'][card_id] <= 0:
        raise RuntimeError('This user does not own the given card!')
    deleted = False
    user['cards'][card_id] -= 1
    if user['cards'][card_id] == 0:
        del user['cards'][card_id]
        deleted = True
    USER_DB.update({'cards': user['cards']}, USER.id == receiving_user)

    # Update CARD_TO_USER_ID
    tups = CARD_TO_USER_ID[card_id]
    index = [i for i in range(len(tups)) if tups[i][0] == receiving_user][0]
    if deleted:
        del tups[index]
    else:
        tups[index] = (receiving_user, user['cards'][card_id])
    CARD_TO_USER_ID[card_id] = tups

'''
Set the image url for the card with the given id.
'''


def gex_set_image(user, card_id, card_image_url):
    gex_util.check_for_card(user, card_id)
    CARD_DB.update(operations.set('image', card_image_url), CARD.id == card_id)

'''
Create a gex card with the given id, masters list, and description.
'''


def gex_create(card_id, card_masters, card_desc=None):
    gex_util.check_user_in_db(card_masters[0])
    time_millis = gex_util.get_time_millis()
    user_data = gex_util.get_user(card_masters[0])
    old_time = 0
    if 'last_create_time' in user_data and user_data['last_create_time'] is not None:
        old_time = user_data['last_create_time']
    if any(user_id in GOD_IDS for user_id in card_masters):
        # for testing and automated card creations, bots don't need to timeout
        old_time = 0
    if time_millis - old_time < 1000 * 60 * 60:  # millis in an hour
        raise RuntimeError('Can only create a card every hour.')
    if not card_masters or not len(card_masters):
        raise RuntimeError('No master provided for this card.')
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if len(matching_cards):
        raise RuntimeError('A card already exists with this id.')
    if len(card_id) > MAX_CARD_ID_LENGTH:
        raise RuntimeError(
            'A card id may be no longer than {} chars.'.format(MAX_CARD_ID_LENGTH))
    CARD_DB.insert({
        'id': card_id,
        'masters': card_masters,
        'desc': card_desc,
        'image': None,
    })
    USER_DB.update({'last_create_time': time_millis},
                   USER.id == card_masters[0])
    CARD_TO_USER_ID[card_id] = []

'''
Get a list of all of the cards a user has, sorted by their occurances.
'''


def gex_flex(user_id):
    gex_util.check_user_in_db(user_id)
    data = gex_util.get_user(user_id)
    cards = data['cards']
    card_keys = list(cards)
    card_keys.sort()
    card_keys.sort(key=lambda x: cards[x], reverse=True)
    card_tuples = []
    for c in card_keys:
        card_tuples.append((c, cards[c]))
    return card_tuples

'''
Get information about the card with the given id.
'''


def gex_inspect(card_id):
    matching_cards = CARD_DB.search(CARD.id == card_id)
    if not matching_cards:
        raise RuntimeError('No card exists with the given id.')
    return matching_cards[0]

'''
Get a lits of all users, and some data about their cards.
'''


def gex_decks():
    users = USER_DB.all()
    ans = []
    for user in users:
        user_id = user['id']
        cards = user['cards']
        unique = len(cards)
        if unique == 0:
            continue
        total = sum(cards.values())
        last_card = None
        if 'last_card' in user:
            last_card = user['last_card']
        ans.append((user_id, unique, total, last_card))
    ans.sort(key=lambda x: x[0])
    ans.sort(key=lambda x: x[2], reverse=True)
    ans.sort(key=lambda x: x[1], reverse=True)
    return ans

'''
Get a list of all existing cards in alphabetical order.
'''


def gex_codex():
    cards = CARD_DB.search(CARD.id.exists())
    print(cards)
    card_ids = [card['id'] for card in cards]
    card_ids.sort()
    return card_ids

# Private message-based funcs


def _gex_give(bot, args, author_id, thread_id, thread_type):
    if not args or len(args) != 2:
        raise RuntimeError(
            'Need to provide command in the form give USER CARD_ID .')
    user_id = gex_util.user_name_to_id(bot, args[0])
    card_id = args[1]
    gex_give(author_id, card_id, user_id)
    # TODO(iandioch): Notify user they got a new card.


def _gex_remove(bot, args, author_id, thread_id, thread_type):
    if not args or len(args) != 2:
        raise RuntimeError(
            'Need to provide command in the form remove USER CARD_ID .')
    user_id = gex_util.user_name_to_id(bot, args[0])
    card_id = args[1]
    gex_remove(author_id, card_id, user_id)
    # TODO(iandioch): Notify user they lost a card.


def _gex_set_image(bot, args, author_id, thread_id, thread_type):
    if not args or len(args) == 1:
        raise RuntimeError(
            'Need to provide command in the form set_image ID URL .')
    card_id = args[0]
    card_image = ' '.join(args[1:])
    try:
        bot.sendRemoteImage(card_image, thread_id=thread_id,
                            thread_type=thread_type)
    except Exception:
        bot.sendMessage('There was an issue sending this image (nsfw?), please choose another.',
                        thread_id=thread_id, thread_type=thread_type)
        return
    gex_set_image(author_id, card_id, card_image)
    bot.sendMessage('Image successfully set to {}'.format(
        card_image), thread_id=thread_id, thread_type=thread_type)


def _gex_create(bot, args, author_id, thread_id, thread_type):
    if not args:
        raise RuntimeError(
            'Need to provide command in the form create ID [DESC] .')
        return
    card_id = args[0]
    card_desc = None
    if len(args) > 1:
        card_desc = ' '.join(args[1:])
    gex_create(card_id, [author_id], card_desc)
    bot.sendMessage('Card {} created.'.format(card_id),
                    thread_id=thread_id, thread_type=thread_type)


def _gex_flex(bot, args, author_id, thread_id, thread_type):
    user_id = author_id
    if len(args):
        user_id = gex_util.user_name_to_id(bot, args[0])
    cards = gex_flex(user_id)
    total = sum(c[1] for c in cards)
    name = gex_util.user_id_to_name(bot, user_id)
    output = '{}\nID: _{}_\n'.format(bold(name), user_id)
    output += 'Total cards: _{}_ (_{}_ unique)\n'.format(total, len(cards))
    output += '\n' + bold('Cards') + ':\n'
    for card, num in cards:
        output += '{}: {}\n'.format(monospace(card[:MAX_CARD_ID_LENGTH]), num)
    bot.sendMessage(output, thread_id=thread_id, thread_type=thread_type)


def _gex_inspect(bot, args, author_id, thread_id, thread_type):
    if not args:
        raise RuntimeError('Need to provide a card id.')
    deets = gex_inspect(args[0])
    print(deets)
    if deets['image'] and deets['image'] is not None:
        print('inspecting image', deets['image'])
        bot.sendRemoteImage(
            deets['image'], thread_id=thread_id, thread_type=thread_type)
    info = '*{}*\n'.format(bold(deets['id']))
    if deets['desc'] is not None:
        info += '{}\n\n'.format(italic(deets['desc']))
    masters = [gex_util.user_id_to_name(bot, master)
               for master in deets['masters']]
    info += 'Masters:\n' + ',\n'.join(masters)
    if deets['id'] in CARD_TO_USER_ID:
        owner_quants = CARD_TO_USER_ID[deets['id']]
        owner_quants = sorted(owner_quants, key=lambda x: x[1], reverse=True)
        owners = [gex_util.user_id_to_name(
            bot, owner_quant[0]) for owner_quant in owner_quants]
        info += '\n\nOwners:\n' + ',\n'.join(owners)
    bot.sendMessage(info, thread_id=thread_id, thread_type=thread_type)


def _gex_decks(bot, args, author_id, thread_id, thread_type):
    users = gex_decks()
    format_str = '{:<16} {:>4} {:>5} {:>' + str(MAX_CARD_ID_LENGTH) + '}'
    out_strings = [format_str.format('Name', 'Uniq', 'Total', 'Most recent')]
    for user_id, unique, total, last_card in users:
        name = gex_util.user_id_to_name(bot, user_id)
        if last_card is None:
            last_card = ''
        name_line = format_str.format(name[:16], str(
            unique), str(total), last_card[:MAX_CARD_ID_LENGTH])
        out_strings.append(name_line)
    out = code_block('\n'.join(out_strings))
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)


def _gex_codex(bot, args, author_id, thread_id, thread_type):
    card_ids = [c[:MAX_CARD_ID_LENGTH] for c in gex_codex()]
    message = '\n'.join(card_ids)
    bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)


def _gex_stats(bot, args, author_id, thread_id, thread_type):
    data = CARD_TO_USER_ID
    number_of_top_cards_to_list = len(data) // 5
    number_of_bottom_cards_to_list = len(data) // 10
    num_owners = {}
    num_in_circulation = {}
    for card in data:
        num_owners[card] = len(data[card])
        num_in_circulation[card] = sum(q[1] for q in data[card])
    most_owned_cards = heapq.nlargest(
        number_of_top_cards_to_list, num_owners, key=lambda x: num_owners[x])
    most_circulated_cards = heapq.nlargest(
        number_of_top_cards_to_list, num_in_circulation, key=lambda x: num_in_circulation[x])
    least_owned_cards = heapq.nsmallest(
        number_of_bottom_cards_to_list, num_owners, key=lambda x: num_owners[x])
    least_circulated_cards = heapq.nsmallest(
        number_of_bottom_cards_to_list, num_in_circulation, key=lambda x: num_in_circulation[x])
    highest_scrabble_scores = heapq.nlargest(
        number_of_top_cards_to_list, data, key=lambda x: _get_scrabble_score(x))
    out = 'Cards owned by the most people (top 20%):'
    FORMAT = '\n{} ({})'
    for card in most_owned_cards:
        out += FORMAT.format(card, num_owners[card])
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)
    out = 'Cards with the most copies in circulation (top 20%):'
    for card in most_circulated_cards:
        out += FORMAT.format(card, num_in_circulation[card])
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)
    out = 'Cards owned by the fewest people (bottom 10%):'
    for card in least_owned_cards:
        out += FORMAT.format(card, num_owners[card])
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)
    out = 'Cards with the fewest copies in circulation (bottom 10%):'
    for card in least_circulated_cards:
        out += FORMAT.format(card, num_in_circulation[card])
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)
    out = 'Cards with the highest scrabble score for their ID (top 20%):'
    for card in highest_scrabble_scores:
        out += FORMAT.format(card, _get_scrabble_score(card))
    bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)


def _gex_help(bot, args, author_id, thread_id, thread_type):
    commands = 'Please use one of the following gex commands, for a low low fee of 5 euroboys:\n' + \
        '\n'.join(sorted(SUBCOMMANDS.keys()))
    bot.sendMessage(commands, thread_id=thread_id, thread_type=thread_type)

SUBCOMMANDS = {
    'give': _gex_give,
    'remove': _gex_remove,
    'set_image': _gex_set_image,
    'create': _gex_create,
    'flex': _gex_flex,
    'inspect': _gex_inspect,
    'decks': _gex_decks,
    'codex': _gex_codex,
    'stats': _gex_stats,
    'help': _gex_help,
    'battle': _gex_battle.battle,
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    print('Running main.')
    if not message:
        # User just typed .gex
        message = 'help'
    subcommand, *args = message.split()
    if subcommand not in SUBCOMMANDS:
        print('subcommand not there', subcommand)
        best_guess = max(SUBCOMMANDS, key=lambda x: difflib.SequenceMatcher(
            None, x, subcommand).ratio())
        bot.sendMessage('Autocorrecting {} to {}'.format(
            subcommand, best_guess), thread_id=thread_id, thread_type=thread_type)
        subcommand = best_guess
    if subcommand in SUBCOMMANDS:
        print('Running command', subcommand)
        try:
            SUBCOMMANDS[subcommand](
                bot, args, author_id, thread_id, thread_type)
            print('done')
        except RuntimeError as e:
            bot.sendMessage('Error while gexin\': {}'.format(
                e), thread_id=thread_id, thread_type=thread_type)
            print(e)
        except Exception as e:
            bot.sendMessage('Misc error: {}'.format(
                e), thread_id=thread_id, thread_type=thread_type)
            print(e)
        return

    bot.sendMessage('Could not find command {}! Gex better son.'.format(
        subcommand), thread_id=thread_id, thread_type=thread_type)

# Things to do at bot boot

_load_card_to_user_id()
