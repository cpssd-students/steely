'''
.roll <dice_string> ...

.roll rolls an arbitrary amount of dice and outputs the result

for example:
.roll 2d20 d20 1d100 ...
'''


import random
import re
from formatting import *


__author__ = 'devoxel'
REPATTERN = re.compile('[\ \W]+')
COMMAND = 'roll'
NLIMIT, RLIMIT = 30, 10000


def roll(n, r):
    '''Returns a formatted string of n roll results between 1 and r'''
    try:
        n = int(n)
        r = int(r)
    except ValueError:
        return None
    if n > NLIMIT or r > RLIMIT or r == 0 or n == 0:
        return None
    s = ' '.join([str(random.randint(1, r)) for i in range(0, n)])
    return '{:<7}| {}'.format(str(n) + 'd' + str(r), s)

def parse_roll(r):
    '''Take a string that should look like: NdR and parse it'''
    r = r.split('d')
    if len(r) > 2:
        return None
    elif len(r) == 1:
        return roll(1, r[0])
    if len(r[0]) == 0:
        return roll(1, r[1])
    return roll(r[0], r[1])

def dorolls(s):
    rolls = REPATTERN.sub('', s).split(' ')[:NLIMIT]
    out = []
    for r in rolls:
        o = parse_roll(r)
        if o is not None:
            out.append(o)
    if len(out) == 0:
        return 'No valid rolls scrub'
    return code_block('\n'.join(out))

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(dorolls(message), thread_id=thread_id, thread_type=thread_type)
