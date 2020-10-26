import datetime
import random

from collections import namedtuple

from plugins.intern.db import *
from plugins.intern.task import *
from plugins.linden import get_balance, handle_intern_earnings


def create_task_for_intern(intern_: Intern):
    def _lerp(domain_lo, domain_hi, range_lo, range_hi, value):
        return (range_lo + (value - domain_lo) * (range_hi - range_lo) /
                (domain_hi - domain_lo))
    options = [TaskType.DOSSING, TaskType.STUDYING, TaskType.INVESTING]
    weights = [10 - _lerp(1, 5, 1, 10, intern_.focus),
               intern_.focus,
               _lerp(1, 5, 1, 10, intern_.focus)]

    print('for intern:')
    print(Intern.serialize(intern_))
    print('options: ', options)
    print('weights: ', weights)

    task_type = random.choices(options, weights=weights, k=1)[0]

    t = Task()
    t.start_time = datetime.datetime.now(datetime.timezone.utc)
    task_duration = datetime.timedelta(minutes=
        _lerp(1, 5, 90, 45, intern_.efficiency))
    t.end_time = t.start_time + task_duration
    t.type_ = task_type
    print('duration: ', task_duration)
    print(t.type_)
    return t

def get_investment_result(intern_: Intern):
    InvestmentResult = namedtuple('InvestmentResult', 'Bad Ok Good')
    options = [InvestmentResult.Bad, InvestmentResult.Ok, InvestmentResult.Good]
    weights = [3 + (5 - intern_.intelligence)*2, 5, 3 + intern_.intelligence]
    result = random.choices(options, weights=weights, k=1)[0]

    num = 0
    status = ''
    if result is InvestmentResult.Bad:
        num = -random.randint(3, 20)
        if get_balance(intern_.manager) + num < 0:
            return f"{intern_.name} tried to invest your Lindens, but you didn't have enough..."
        status = f'{intern_.name} followed a penny stock investment strategy they found on /r/wsb, and lost {num} lindens.'
    elif result is InvestmentResult.Ok:
        num = random.randint(2, 22)
        status = f'{intern_.name} randomly bought and sold some shares, and gained {num} lindens.'
    elif result is InvestmentResult.Good:
        num = random.randint(20, 100)
        status = f'{intern_.name} studied the earnings of some oil companies, made a smart bet, and earned {num} lindens.'

    handle_intern_earnings(intern_.manager, num)
    return status




def get_busy_string(intern_: Intern, task_type: TaskType):
    # TODO(iandioch): It might be good to associate this with a Task, instead of
    # it appearing differently for each "/intern check" call.
    name = intern_.name
    STRS = {
        TaskType.DOSSING: [
            f'{name} is staring into space contentedly.',
            f'{name} is slacking off by writing a Steely plugin.',
            f'{name} is asleep at their desk.',
            f'{name} is outside having a smoke.',
        ],
        TaskType.STUDYING: [
            f'You see that {name} has 40 StackOverflow tabs open, and looks a bit flustered.',
            f'{name} looks to be reading a Medium article and sharing it on LinkedIn with a very long personal story attached.',
            f'{name} is reading the manpage for `man`.',
            f'{name} is looking at a book on Amazon entitled "Interning for Dummies".',
            f'{name} is watching a programming tutorial on Youtube in Hindi.',
        ],
        TaskType.INVESTING: [
            f'{name} has an doc open in front of them, titled "Due Diligence". The rest of the doc is empty.',
            f'{name} just punched some numbers into a calculator. You see over their shoulder the calculator display reads 58008.',
            f'{name} is watching a horseracing stream and clutching a ticket desperately.',
            f'{name} is signing up to a pyramid scheme. You should probably warn them...',
        ],
    }
    return random.choice(STRS[task_type])


def check(intern_: Intern):
    if random.random() < 0.05:
        # If you check often on your intern, their focus will increase.
        intern_.focus = min(intern_.focus + 1, 5)
        update_intern(intern_)

    # TODO(iandioch): Potentially expire intern, if they are old.
    # TODO(iandioch): Check if intern has been paid, etc.

    # Intern has no task. Should only be the case for newly created interns?
    if intern_.task is None:
        intern_.task = create_task_for_intern(intern_)
        update_intern(intern_)
        return f'{intern_.name} just started doing something.'
    task = intern_.task

    print('end time: ', task.end_time)
    print('now: ', datetime.datetime.now(datetime.timezone.utc))

    # Intern is not finished current task.
    if task.end_time > datetime.datetime.now(datetime.timezone.utc):
        return get_busy_string(intern_, task.type_)

    # Intern finished their previous task too long ago, now they're doing nothing.
    if (datetime.datetime.now(datetime.timezone.utc) -
            datetime.timedelta(hours=6) > task.end_time):
        intern_.task = create_task_for_intern(intern_)
        # If the intern is not checked on for a while, their focus can decrease.
        if random.random() < 0.2:
            intern_.focus = max(intern_.focus - 1, 1)
        update_intern(intern_)
        return f'{intern_.name} was busy earlier, but seems to have been sitting around since then.'

    # Give intern new task.
    intern_.task = create_task_for_intern(intern_)
    update_intern(intern_)

    # Intern finished their previous task and now will present their results:
    if task.type_ is TaskType.DOSSING:
        return f'You see {intern_.name} has doodled a pretty picture.'
    if task.type_ is TaskType.STUDYING:
        s = get_busy_string(intern_, task.type_)
        if intern_.intelligence < 5 and random.random() < 0.5:
            return s + '\n' + f"{intern_.name}'s intelligence increased."
        return s
    if task.type_ is TaskType.INVESTING:
        return get_investment_result(intern_)
