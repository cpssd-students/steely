import random
import uuid
from typing import Union

from tinydb import Query
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from formatting import *
from utils import new_database
from plugin import create_plugin 

HELP_STR = """
"""
plugin = create_plugin(name='intern', author='iandioch', help=HELP_STR)

DATABASE = None
INTERN = Query()

NUM_UNHIRED_INTERNS = 3

class Intern:
    # User-facing name ("Cian Ruane").
    name: str
    # Internal-only name ("1290934").
    id_: str

    # Stats. All on a scale of 1-5.
    # Influences how good they are at doing tasks.
    intelligence: int
    # Influences how quickly they will do a task and move on.
    efficiency: int
    # Influences how often they will do a useful task. Naturally degrades, but
    # can increase if the intern is often checked on.
    focus: int

    # User ID of this intern's manager (ie. someone in a chat).
    # None means this intern is on the job market.
    manager: Union[str, None] = None

    @staticmethod
    def serialize(intern_) -> str:
        d = {
            'name': intern_.name,
            'id_': intern_.id_,
            'type': 'intern',
            'intelligence': intern_.intelligence,
            'focus': intern_.focus,
            'efficiency': intern_.efficiency,
        }
        if intern_.manager is not None:
            d['manager'] = intern_.manager
        return d

    @staticmethod
    def deserialize(obj):
        n = Intern()
        n.name = obj['name']
        n.id_ = obj['id_']
        n.intelligence = obj['intelligence']
        n.focus = obj['focus']
        n.efficiency = obj['efficiency']
        n.manager = obj['manager'] if 'manager' in obj else None
        return n

    @staticmethod
    def generate():
        def generate_name() -> str:
            # TODO(iandioch): Make a proper list of firsts + lasts.
            return random.choice('abcdefgh') + ' ' + random.choice('abcdefgh')
        n = Intern()
        n.name = generate_name()
        n.id_ = uuid.uuid4().hex
        n.intelligence = random.randint(1,5)
        n.focus = random.randint(1,5)
        n.efficiency = random.randint(1,5)
        return n


def _get_intern(intern_id: str) -> Union[Intern, None]:
    res = DATABASE.search(INTERN.id_ == intern_id)
    if not len(res):
        return None
    return Intern.deserialize(res[0])


def _update_intern(intern_: Intern):
    DATABASE.upsert(Intern.serialize(intern_), INTERN.id_ == intern_.id_)


def _get_intern_for_manager(user_id: str) -> Union[Intern, None]:
    res = DATABASE.search(INTERN.manager == user_id)
    if not len(res):
        return None
    return Intern.deserialize(res[0])


def _get_unhired_interns():
    while True:
        unhired = DATABASE.search(~(INTERN.manager.exists()))
        # If there aren't enough interns on the market, add them one at a time
        # until there are.
        if len(unhired) < NUM_UNHIRED_INTERNS:
            new_intern = Intern.generate()
            DATABASE.insert(Intern.serialize(new_intern))
            continue

        interns = [Intern.deserialize(u) for u in unhired]
        interns.sort(key = lambda x: x.name)
        return interns


def _render_intern_info(intern_: Intern) -> str:
    def render_stars(n: int) -> str:
        return '★'*n
    return f"""{bold("name")}: {intern_.name}
{bold("intelligence")}: {render_stars(intern_.intelligence)}
{bold("efficiency")}: {render_stars(intern_.efficiency)}
{bold("focus")}: {render_stars(intern_.focus)}"""

@plugin.setup()
def setup():
    global DATABASE 
    DATABASE = new_database('intern')

@plugin.listen(command='intern hire [intern_id]')
def hire(bot, message, **kwargs):
    if 'intern_id' in kwargs and kwargs['intern_id'] != '':
        intern_id = kwargs['intern_id']
        intern_ = _get_intern(intern_id)
        hirer = bot.fetchUserInfo(message.author_id)[0]
        bot.sendMessage('{} is hiring intern {}.'.format(hirer['full_name'],
                                                         intern_.name),
                        thread_id=message.thread_id,
                        thread_type=message.thread_type)
        if intern_.manager is not None:
            bot.sendMessage('{} is already hired!'.format(intern_.name),
                            thread_id=message.thread_id,
                            thread_type=message.thread_type)
            return
        if _get_intern_for_manager(message.author_id) is not None:
            bot.sendMessage('{} already has an intern!'.format(
                                hirer['first_name']),
                            thread_id=message.thread_id,
                            thread_type=message.thread_type)
            return
        intern_.manager = message.author_id
        _update_intern(intern_)
        return

    unhired_interns = _get_unhired_interns()
    intern_detail_strs = []
    button_list = []
    for unhired in unhired_interns:
        # Creates a button saying "Hire XYZ", that will send a command of the
        # form '/intern hire {intern_id}' when clicked.
        callback_data = '/intern hire {}'.format(unhired.id_)
        button_list.append([
            InlineKeyboardButton('Hire {}'.format(unhired.name),
                                 callback_data=callback_data)
        ])
        intern_detail_strs.append(_render_intern_info(unhired))

    reply_markup = InlineKeyboardMarkup(button_list, n_cols=1)
    bot.sendMessage('\n---\n'.join(intern_detail_strs),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type,
                    reply_markup=reply_markup)

@plugin.listen(command='intern check')
def check(bot, author_id, message, thread_id, thread_type, **kwargs):
    pass
