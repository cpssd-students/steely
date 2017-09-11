'''
.slag <name>
slags a person in the chat

.slag add "Shut up {}"
adds a slag to the chat.

added slags are temporary and fleeting.

.slag <rip|sam|rm>
you should know how these work already
'''


import random

__author__ = 'devoxel'
COMMAND='.slag'

DEVOXEL_ID = 100005463364685

def load_slags():
    SLAGS_FILENAME = "databases/slags"
    with open(SLAGS_FILENAME) as f:
        x = f.read()
    return set(x.split("\n"))

class SlagDB:
    def __init__(self, loaded_slags):
        self.on = True
        self.__base_slags = frozenset([
            "{} you absolute walnut",
            "Shut up {}",
        ]) | loaded_slags
        self.gods = [DEVOXEL_ID]
        self.clear(DEVOXEL_ID)
        # slag permissions: [devoxel, ]

    def add(self, s):
        # maybe do a sentiment check eventually lol
        if not self.on or s.count("{}") != 1:
            return False
        self.slags.add(s)
        return True

    def clear(self, uid):
        if int(uid) in self.gods:
            self.slags = set(self.__base_slags)
            return True
        return False

    def remove(self, search, uid):
        # this method is slow and badly written but not arsed
        if int(uid) not in self.gods:
            return False
        rm = []
        for s in self.slags:
            if search in s:
                rm.append(s)
        self.slags -= set(rm)
        self.slags |= self.__base_slags
        return True

    def toggle(self, uid):
        # returns IS_GOD, self.on
        if uid in self.gods:
            self.on = not self.on
            return True, self.on
        return False, None

SLAGDB = SlagDB(load_slags())

# these functions stay silent on empty return values
# maybe change this

def add(s):
    if SLAGDB.add(s):
        return "okay sam" # maybe make this quiet
    return "no >:(. {} is not valid".format(s)

def clear(uid):
    if SLAGDB.clear(uid):
        return "this is why we can't have nice things"
    return "ecks dee"

def remove(s, uid):
    if SLAGDB.remove(s, uid):
        return "delet this"
    return "no"

def slag(name):
    # only command to not use a slagdb method so just use SLAGDB.on directly
    if not SLAGDB.on:
        return False # stay silent
    s = random.sample(SLAGDB.slags, 1)[0]
    try:
        return s.format(name)
    except ValueError:
        return "some arsehole left a bad slag: " + s

def toggle(uid):
    ok, on = SLAGDB.toggle(uid)
    if not ok:
        return False
    if not on:
        return "dab on the haters"
    else:
        return ">:("

def handle(message, uid):
    message = message.strip()

    # this is my super lazy way of doing commands
    # they HAVE to be length 3
    cmd = message[:4].strip().lower()
    cmd_msg = message[3:].strip()

    if len(cmd) == 0:
        return "cant even type a command correctly jfc"
    if cmd == "add":
        return add(cmd_msg)
    elif cmd == "rip":
        return clear(uid)
    elif cmd == "del":
        return remove(cmd_msg, uid)
    elif cmd == "sam":
        return toggle(uid)
    else:
        return slag(message)

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    out = handle(message, author_id)
    if out:
        bot.sendMessage(out, thread_id=thread_id, thread_type=thread_type)

if __name__ == "__main__":
    # move these into a test thing sometime or something

    # test slag does something
    assert "noah" in slag("noah")

    # test add
    s = "noice {}"
    handle("add " + s, 12)
    assert s in SLAGDB.slags

    # test del
    handle("del ice", 13)
    assert s in SLAGDB.slags
    handle("del ice", DEVOXEL_ID)
    assert s not in SLAGDB.slags

    # test clear
    handle("add " + s, 12)
    assert s in SLAGDB.slags
    handle("rip", 12)
    assert s in SLAGDB.slags
    handle("rip", DEVOXEL_ID)
    assert s not in SLAGDB.slags and len(SLAGDB.slags) > 0

    # test quiet
    assert toggle(DEVOXEL_ID) == "dab on the haters" # toggle
    assert slag("noah") == False
    handle("add " + s, 12)
    assert s not in SLAGDB.slags
    handle("sam", 12) # toggle again
    handle("add " + s, 12)
    assert s not in SLAGDB.slags
    handle("sam", DEVOXEL_ID)
    handle("add " + s, 12)
    assert s in SLAGDB.slags

    # test slags init
    asdf = SlagDB(set([s]))
    assert s in asdf.slags
