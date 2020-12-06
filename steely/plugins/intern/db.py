import random
import uuid
from typing import Union

import requests

from tinydb import Query

from formatting import *
from utils import new_database
from plugins.intern.task import Task

DATABASE = None
INTERN = Query()

NUM_UNHIRED_INTERNS = 3

def setup_database():
    global DATABASE
    DATABASE = new_database('intern')


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

    task: Union[Task, None] = None

    @staticmethod
    def serialize(intern_):
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
        if intern_.task is not None:
            d['task'] = Task.serialize(intern_.task)
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
        n.task = Task.deserialize(obj['task']) if 'task' in obj else None
        return n

    @staticmethod
    def generate():
        def generate_name() -> str:
            URL = 'http://names.drycodes.com/1'
            data = requests.get(URL).json()
            return data[0].replace('_', ' ')
        n = Intern()
        n.name = generate_name()
        n.id_ = uuid.uuid4().hex
        n.intelligence = random.randint(1,5)
        n.focus = random.randint(1,5)
        n.efficiency = random.randint(1,5)
        return n


def get_intern(intern_id: str) -> Union[Intern, None]:
    res = DATABASE.search(INTERN.id_ == intern_id)
    if not len(res):
        return None
    return Intern.deserialize(res[0])


def update_intern(intern_: Intern):
    DATABASE.upsert(Intern.serialize(intern_), INTERN.id_ == intern_.id_)


def get_intern_for_manager(user_id: str) -> Union[Intern, None]:
    res = DATABASE.search(INTERN.manager == user_id)
    if not len(res):
        return None
    return Intern.deserialize(res[0])


def get_unhired_interns():
    # Sorted by name.
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


def get_hired_interns():
    resp = DATABASE.search(INTERN.manager.exists())
    yield from (Intern.deserialize(u) for u in unhired)


def render_intern_info(intern_: Intern) -> str:
    def render_stars(n: int) -> str:
        return '★'*n
    return f"""{bold("name")}: {intern_.name}
{bold("intelligence")}: {render_stars(intern_.intelligence)}
{bold("efficiency")}: {render_stars(intern_.efficiency)}
{bold("focus")}: {render_stars(intern_.focus)}""" 
