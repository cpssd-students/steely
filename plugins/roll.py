"""
Example:

.roll 2d20 d20 1d100 ...
"""
import random

COMMAND = '.roll'
NLIMIT, RLIMIT = 999, 999


def roll(n, r):
    """Returns a formatted string of n roll results between 1 and r"""
    try:
        n = int(n)
        r = int(r)
    except ValueError:
        return None
    if n > NLIMIT or r > RLIMIT:
        return None
    s = ' '.join([str(random.randint(1, r)) for i in range(0, n)])
    return '{:<7}| {}'.format(str(n) + 'd' + str(r), s)

def parse_roll(r):
    """Take a string that should look like: NdR and parse it"""
    r = r.split('d')
    if len(r) > 2:
        return None
    elif len(r) == 1:
        return roll(1, r[0])
    if len(r[0]) == 0:
        return roll(1, r[1])
    return roll(r[0], r[1])

def dorolls(s):
    rolls = s.split(' ')
    if len(rolls) > 25:
        return 'Too many rolls!'
    out = []
    for r in rolls:
        o = parse_roll(r)
        if o is not None:
            out.append(o)
    if len(out) == 0:
        return 'No valid rolls scrub'
    return "```" + '\n'.join(out) + "```"

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(dorolls(message), thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
	print(dorolls('4d20 10d100 1d6 2d8'))
