from __future__ import annotations

import llm
import re
from random import choice
from typing import Optional, NamedTuple, Type, TypeVar, Tuple, Any, Callable
from random import random, randint
import time
import typing
from collections import deque
import logging
import hashlib
from tinydb import Query, TinyDB
from tinydb.storages import MemoryStorage

from utils import new_database
from plugin import create_plugin
from message import SteelyMessage
from paths import CONFIG

logger = logging.getLogger(__name__)

HELP_STR = """
sam is an ai friend or foe.
sam takes many forms.
sam is a spy.
opt in to sam today.

Usage:
- sam spy - toggle data collection
- sam treat - reward sammy with a treat
- sam scold - scold sammy for being a prick
- sam kill [new sam instructions] - sam moves away and a new sam will return in time
- sam [message] - directly address sam
"""

# this is a helper func to serialize namedtuples easily from TinyDB/dict representation
T = TypeVar('T', bound=NamedTuple)
def tuple_from_dict(obj: Type[T], d: dict[typing.Any, typing.Any]) -> T:
    new = []
    for f in obj._fields:
        v = d.get(f)
        if v is None:
            if f not in obj._field_defaults:
                raise ValueError(f"field {f} required for {type(obj)}")
            v = obj._field_defaults[f]
        new.append(v)
    return obj._make(new)

class SamTraits(NamedTuple):
    name: str
    bio: str
    age: str
    location: str
    bond: str
    flaw: str
    trait: str
    flair: str
    style: str
    intro: str
    chattyness: str
    emotion: str

class SamState(NamedTuple):
    hp: int = 10
    treats: int = 0
    scolds: int = 0
    default_emotion: str = "Curious"
    emotion: str = "Excited"
    last_response_time: float = time.time()
    chat_mod: float = 0

    def kill(self) -> SamState:
        return self._replace(hp=-1)

    def wound(self) -> SamState:
        return self._replace(hp=0)

    def reset_emotion(self) -> SamState:
        return self._replace(emotion=self.default_emotion)

    def scold(self) -> SamState:
        return self._replace(hp=self.hp - randint(1, 3), scolds = self.scolds+1)

    def treat(self) -> SamState:
        return self._replace(hp=self.hp + randint(1, 3), treats = self.treats+1)

def new_state(trait: SamTraits) -> SamState:
    d: dict[str, Any] = {"default_emotion": trait.emotion}
    try:
        cm = float(trait.chattyness.strip())
        cm = cm/10 # scale to 0 -> 1
        if cm < 0 or cm > 1:
            logger.info("AI gave bad chattyness: %s", trait.chattyness)
            raise ValueError
        cm = (cm - .5)/3
        d["chat_mod"] = cm
    except ValueError:
        pass
    return SamState()._replace(**d)

class AI():
    RE = re.compile(r"(?P<key>@[a-zA-Z]+)(?P<val>[^@]*)", flags=re.MULTILINE)

    SAM_DESC = SamTraits(name="The character's full name - the first name must begin with Sam",
                   bio="A very short bio about your character",
                   age="The characters age",
                   location="The location where your character is currently from. Could be a real country or fantasy location",
                   bond="Something the character cares about deeply",
                   flaw="A personality weakness your character has",
                   flair="A unique item your character has",
                   style="Your texting style",
                   trait="A unique trait the character posses",
                   intro="A short, single sentance introduction message to the group",
                   chattyness="A number between 0 and 10 that indicates how often you reply",
                   emotion="A description of an emotional state people are likely to find you in")

    SAM_DEFAULT = SamTraits(name="Samwise Dickens",
                       bio="Samwise is an ex-male model who has taken to studying philosophy.",
                       age="35",
                       location="Berlin.",
                       bond="always wants to be looking good",
                       flaw="a little bit narcissitic",
                       style="terse but slightly romantic",
                       flair="commemerative Al Gore Hat",
                       trait="always ends their messages in 'hahah'",
                       intro="well hello friends",
                       chattyness="4",
                       emotion="Cool as a cucumber")

    def __init__(self):
        self.model = llm.get_model("gpt-3.5-turbo")
        self.model.key = CONFIG.OPENAI_KEY

    @staticmethod
    def parse_samdef(proto: dict[str, str|None], inp: str) -> dict[str, str]:
        d = {}
        for k, v in proto.items():
            if v is not None:
                d[k] = v
        for match in AI.RE.finditer(inp):
            kw = match.group("key")[1:]
            val = match.group("val").strip()
            if len(val) == 0:
                logger.info("ai gave an empty value for: %s", kw)
                continue
            if kw in proto:
                d[kw] = val
            else:
                logger.info("ai hallucinated a keyword: %s", kw)
        return d

    @staticmethod
    def prompt_new_sam(suggestion: str) -> str:
        seeds = [ # yes some of these are mutually exclusive, more interesting that way I say
            "create somebody inspired",
            "make the character funny in an adult-swim kinda way",
            "take inspiration from Irish (but not a steriotype)",
            "give them a great accent",
            "make them snooty and uncouth",
            "make them from somewhere interesting on earth",
            "make them a somebody from a small town",
            "make them too big for their boots",
            "give them a powerful aura",
            "make them a master of code",
            "make them something fantasy inspired; without being lame",
            "make them really want to impress everybody",
            "do something meta",
            "make them working class",
            "have their background be upper class",
            "have their background be working class",
            "make their backgroun be lower class",
            "with a very distinct texting style",
            "always chill with people, no matter what",
            "willing to break outside of the mold",
            "wants to start flame wars",
        ]
        if len(suggestion) == 0:
            fun = []
            for _ in range(3):
                s = choice(seeds)
                seeds.remove(s)
                fun.append(s)
            suggestion = " and ".join(fun).capitalize()
        keywords = "\n".join([f"@{k} {v}" for k, v in AI.SAM_DESC._asdict().items()])
        return f"""You are generating a unique and interesting character for a character
that responds to instant messenger.

You have a guiding prompt, which is: "{suggestion}".
You dont need to work too closely too this prompt, use it as a guide.
Your character's name must begin with Sam.

It is important that the output is generated in a specific format for processing by a computer program.
The format is simple, it is a series of keyword followed by a description.
A keyword is word starting with an @ symbol.

The following keywords are required:
{keywords}
        """

    @staticmethod
    def prompt_sam_response(sam: SamTraits, state: SamState, memory: MessageMemory, situation: str) -> str:
        return f"""You are an interesting character responding to instant messager chats.
You have a character, a personality and some state parameters which you will
use to form the basis for your response. You will speak in the first person.

Remember than in IM, short messages are preferred, unless you have a good
reason for a long message, keep things short but keep the conversation moving.
Remember your personality but dont shoehorn it into every response.

Your name is {sam.name}. {sam.bio}
You are from {sam.location}.
Your bond is {sam.bond} and your flaw is {sam.flaw}.
Your personality trait is: {sam.trait}.
Your texting style is {sam.style}.

Your current emotional state is {state.emotion}.
You gave been given {state.treats} treats and you have been scolded {state.scolds} times.

{situation}

Here is the chain of past messages:
{memory}

You must respond in the following format:

@emotion <emotion>
@response <test response>
    """

    def _respond_to(self, sam: SamTraits, state: SamState, memory: MessageMemory, situation: str) -> tuple[typing.Optional[str], SamState]:
        prompt = AI.prompt_sam_response(sam, state, memory, situation)
        logger.debug("prompt is %s", prompt)
        response = self.model.prompt(prompt)
        logger.debug("response %s", response)
        parsed = AI.parse_samdef({"response": None, "emotion": state.default_emotion}, response.text())
        new_state = state._replace(emotion = parsed["emotion"])
        return (parsed["response"], new_state)

    def new_sam(self, suggestion: str ="") -> SamTraits:
        prompt = AI.prompt_new_sam(suggestion)
        response = self.model.prompt(prompt)
        logger.debug("new sam response %s", response)
        parsed = AI.parse_samdef(AI.SAM_DEFAULT._asdict(), response.text())
        return AI.SAM_DEFAULT._make(parsed.values())

    def chime_in(self, sam: SamTraits, state: SamState, memory: MessageMemory):
        s = "You have seen some messages and would like to respond, either by chiming in or by contining on a seen idea."
        return self._respond_to(sam, state, memory, s)

    def scold(self, sam: SamTraits, state: SamState, memory: MessageMemory) -> tuple[typing.Optional[str], SamState]:
        who = memory.last_user()
        s = f"{who.username()} scolded you! That probably angers you, and you want to get a response in."
        return self._respond_to(sam, state, memory, s)

    def treat(self, sam: SamTraits, state: SamState, memory: MessageMemory) -> tuple[typing.Optional[str], SamState]:
        who = memory.last_user()
        s = f"You got a treat from {who.username()}! This improves your mood and you would like to respond!"
        return self._respond_to(sam, state, memory, s)

    def goodbye(self, sam: SamTraits, state: SamState, memory: MessageMemory) -> typing.Optional[str]:
        s = "You are leaving the chat for some reason. Invent the reason why, and if you can, incorporate the message chain."
        resp, _ =  self._respond_to(sam, state, memory, s)
        return resp

    def respond(self, sam: SamTraits, state: SamState, memory: MessageMemory) -> tuple[typing.Optional[str], SamState]:
        who = memory.last_user()
        # god this is ugly
        s = f"""
You have been directly asked a question. The most recent message in the chain is directly addressed to you from {who.username()}.
""".strip()
        return self._respond_to(sam, state, memory, s)

class SamDB():
    def __init__(self, db: TinyDB):
        self.version = 1
        self.db = db.table("sams")

    def _get(self, hash: str):
        sam = Query()
        sams = self.db.search(sam.hash == hash)
        if len(sams) > 1:
            logger.error("more than one sam for given hash in db")
            return self.delete(hash)
        if len(sams) == 0:
            return None
        return sams[0]

    def write(self, hash: str, traits: SamTraits, state: SamState):
        d = { 'hash': hash, 'traits': traits._asdict(), 'state': state._asdict() }
        sam = Query()
        return self.db.upsert(d, sam.hash == hash)

    def delete(self, hash: str):
        sam = Query()
        self.db.remove(sam.hash == hash)

    def get(self, hash: str) -> typing.Tuple[SamTraits, SamState]:
        sam = self._get(hash)
        if sam is None:
            logger.debug("could not find sam in db")
            return (AI.SAM_DEFAULT, SamState().kill())
        trait_dict: dict[str, typing.Any] = sam["traits"]
        state_dict: dict[str, typing.Any] = sam["state"]
        try:
            traits = tuple_from_dict(SamTraits, trait_dict)
            state =  tuple_from_dict(SamState, state_dict)
        except ValueError:
            logger.exception("could not deserialize samdb entry")
            self.delete(hash)
            return (AI.SAM_DEFAULT, SamState().kill())
        return (traits, state)

def index(msg: SteelyMessage) -> str:
    m = hashlib.md5()
    for k in [msg.thread_id, msg.thread_type]:
        m.update(hashlib.md5(str.encode(str(k))).digest())
    return hashlib.md5().hexdigest()

class User(NamedTuple):
    id: typing.Any
    real_username: str
    anon_username: str = ""
    tracked: bool = False

    def username(self) -> str:
        if self.anon_username:
            return self.anon_username
        return self.real_username

class UserDB():
    def __init__(self, db: TinyDB):
        self.db = db.table("users")

    def update(self, user: User):
        users = Query()
        print(self.db.all())
        updated = self.db.upsert(user._asdict(), users.id == user.id)
        assert(len(updated) <= 1)

    def get_or_add(self, bot, message: SteelyMessage) -> User:
        users = Query()
        info = bot.fetchUserInfo(message.author_id)
        assert(len(info) == 1)
        umap = info[0]

        docs = self.db.search(users.id == umap["id"])
        if len(docs) == 0:
            user = User(message.author_id, umap["username"])
            self.db.upsert(user._asdict(), users.id == message.author_id)
            return user

        assert(len(docs) == 1)
        return tuple_from_dict(User, docs[0])

class MessageMemory:
    def __init__(self, buflen):
        self.msgbuf: deque[Tuple[User, str]] = deque(maxlen=buflen)

    def last_user(self) -> User:
        return self.msgbuf[-1][0]

    def append(self, user: User, msg: str):
        self.msgbuf.append((user, msg))

    def clear(self):
        self.msgbuf.clear()

    def __str__(self) -> str:
        return "\n".join([f"{u.username()}: {msg}" for u, msg in self.msgbuf])

# SamNonAbstractBeanMachineMaker()
class SamManager():
    MESSAGE_HISTORY = 10

    # note that interacting with the bot will temporarily increase the value
    CHANCE_RESPAWN = .5 # chance to respawn given each message
    CHANCE_RESPONSE = .05
    CHANCE_REACT = .4 # to direct messages or scolds/treats
    CHANCE_CONVERSATION_INCREASE = .2

    THRESHOLD_EMOTION_RESET = 60
    THRESHOLD_CONVERSATION_SECONDS = 120

    # cap on likelyhood to respond
    THRESHOLD_CHANCE_SPAM = .5

    def __init__(self):
        self.ai = AI()
        db = new_database("sam.db")
        self.samdb = SamDB(db)
        self.users = UserDB(db)
        self.memory: dict[str, MessageMemory] = {}
        logger.setLevel(logging.DEBUG) # TODO: REMOVE

    def spy(self, bot, message: SteelyMessage):
        user = self.users.get_or_add(bot, message)
        user = user._replace(tracked=not user.tracked)
        self.users.update(user)
        msg = "Uncle Sam: tracking disabled.\nInclude '(spy)' in you message to get seen anyway."
        if user.tracked:
            msg = "Uncle Sam: tracking enabled.\n" \
                "Your messages will be sent to OpenAI and likely stored forever by Sam Altman. " \
                "Include '(nospy)' in you message to get hide a message."
        bot.sendMessage(msg, thread_id=message.thread_id, thread_type=message.thread_type)

    def _should_respond(self, state: SamState, base: float) -> bool:
        now = time.time()
        chance = base
        chance += state.chat_mod
        # bot likes to have conversations rather than one off messages
        # should probably make this a smooth gradient
        if (state.last_response_time - now) < SamManager.THRESHOLD_CONVERSATION_SECONDS:
            chance += SamManager.CHANCE_CONVERSATION_INCREASE
        chance = max(SamManager.CHANCE_RESPONSE, SamManager.THRESHOLD_CHANCE_SPAM)
        return random() < chance

    def _should_respawn(self) -> bool:
        return random() < SamManager.CHANCE_RESPAWN

    def _setup(self, bot, message: SteelyMessage) -> Tuple[str, MessageMemory, User]:
        hash = index(message)
        memory = self.memory.get(hash)
        if memory is None:
            memory = MessageMemory(SamManager.MESSAGE_HISTORY)
            self.memory[hash] = memory
        user = self.users.get_or_add(bot, message)
        return hash, memory, user

    def _is_tracked(self, user: User, message: SteelyMessage):
        if "(spy)" in message.text:
            return True
        if "(nospy)" in message.text:
            return False
        return user.tracked

    def kill(self, bot, message: SteelyMessage):
        def wound(s: SamState):
            return s.wound() # to get a goodbye message
        self._handle(bot, message, self.ai.chime_in, transform=wound)

    def scold(self, bot, message: SteelyMessage):
        def scold(s: SamState):
            return s.scold()
        self._handle(bot, message, self.ai.scold, transform=scold, chance=SamManager.CHANCE_REACT)

    def treat(self, bot, message: SteelyMessage):
        def treat(s: SamState):
            return s.treat()
        self._handle(bot, message, self.ai.treat, transform=treat, chance=SamManager.CHANCE_REACT)

    def addressed(self, bot, message: SteelyMessage):
        self._handle(bot, message, self.ai.respond, chance=SamManager.CHANCE_REACT)

    def info(self, bot, message: SteelyMessage):
        hash, _, _ = self._setup(bot, message)
        (trait, state) = self.samdb.get(hash)
        response = ""
        if state.hp <= 0:
            response = f"Sam is gone. Use `{CONFIG.COMMAND_PREFIX} sam summon [guidance]` to call forth a new sam."
        else:
            # TODO: would be nice to add some stats, E.G: number of total sams.
            response = "\n".join([f"{trait.name}",
                                  f"Age: {trait.age}",
                                  f"Bond: {trait.bond}",
                                  f"Style: {trait.style}",
                                  f"HP: {state.hp}"])
        bot.sendMessage(f"{response}", thread_id=message.thread_id, thread_type=message.thread_type)

    def listen(self, bot, message: SteelyMessage):
        def maybe_reset(s: SamState):
            if (s.last_response_time - time.time()) < SamManager.THRESHOLD_EMOTION_RESET:
                return s.reset_emotion()
            return s
        if message.text.startswith("f{CONFIG.COMMAND_PREFIX}sam"):
            return # will lead to double responses
        # TODO: maybe filter out commands
        self._handle(bot, message, self.ai.chime_in, transform=maybe_reset)

    def _handle(self, bot, message: SteelyMessage,
            ai: Callable[[SamTraits, SamState, MessageMemory], Tuple[Optional[str], SamState]],
                transform: typing.Optional[Callable[[SamState], SamState]] = None, chance=None):
        hash, memory, user = self._setup(bot, message)

        tracked = self._is_tracked(user, message)
        if not tracked:
            logger.debug("user %s is not tracked", repr(user))
            return

        if chance is None:
            chance = SamManager.CHANCE_RESPONSE

        response = None
        prelude = ""
        (trait, state) = self.samdb.get(hash)

        logger.debug("handling message %s, current sam is: %s, thread: %s", repr(message.text), trait.name, hash)
        logger.debug("current sam state %s", repr(state))

        if transform is not None:
            state = transform(state)
            logger.debug("sam state after transform %s", repr(state))

        # this logic is growing more and more complex.
        # probably should be a proper state machine.
        if state.hp < 0:
            if self._should_respawn():
                (trait, state) = self._new_sam()
                prelude = f"{trait.name} has joined the chat.\n"
                response = trait.intro
                logger.debug("created new sam, state %s", repr(state))
            else:
                return
        elif state.hp == 0:
            response = self.ai.goodbye(trait, state, memory)
            if response is None:
                response = "..."
            response += f"\n\n {trait.name} has left the chat."
            state = state.kill()
            memory.clear()

        if state.hp > 0 and self._should_respond(state, chance):
            memory.append(user, message.text)
            response, state = ai(trait, state, memory)

        if response is not None:
            bot.sendMessage(f"{prelude}{trait.name}: {response}", thread_id=message.thread_id, thread_type=message.thread_type)
            user = User(None, f"{trait.name} (you)")
            memory.append(user, response)

        self.samdb.write(hash, trait, state)
        return

    def _new_sam(self) -> typing.Tuple[SamTraits, SamState]:
        traits = self.ai.new_sam()
        logger.info("generated new sam %s", repr(traits))
        return traits, new_state(traits)

    def debug(self, bot, message: SteelyMessage):
        debug_mode = True # this escapes my linter from getting angry about dead-code.
        if debug_mode:
            raise Exception("debug mode not enabled")
        def p(msg: str, data: Any):
            print(f"\n!! {msg}\n {data}\n\n")

        logger.setLevel(logging.DEBUG)
        sammy = self.ai.new_sam()
        state = new_state(sammy)
        p("ai.new_sam", sammy)

        memory = MessageMemory(10)
        memory.append(User(None, "jim"), "whats the craic joe?")
        memory.append(User(None, "joe"), "ah not much jim, fancy a pint next thursday?")
        p("message memory", memory)

        resp, state = self.ai.chime_in(sammy, state, memory)
        p("chime in response", resp)
        p("chime in state", state)

        hash = index(message)
        p("thread hash", hash)

        db = SamDB(TinyDB(storage=MemoryStorage))

        p("empty db", db.get(hash))

        db.write(hash, sammy, state)
        p("db entry", db.get(hash))

        resp, state = self.ai.scold(sammy, state, memory)
        p("scold", resp)

        resp, state = self.ai.treat(sammy, state, memory)
        p("treat", resp)


plugin = create_plugin(name='sam', author='devoxel', help=HELP_STR)
MANAGER: Optional[SamManager] = None

@plugin.setup()
def plugin_setup():
    global MANAGER
    MANAGER = SamManager()

def ensure_init(f):
    def wrap(*args):
        global MANAGER
        if MANAGER is None:
            # TODO: handle error
            raise Exception("i cant believe youve done this")
        f(MANAGER, *args)
    return wrap

@plugin.listen()
@ensure_init
def listen(manager: SamManager, bot, message: SteelyMessage):
    manager.listen(bot, message)

@plugin.listen(command='sam info')
@ensure_init
def info(manager: SamManager, bot, message: SteelyMessage):
    manager.info(bot, message)

@plugin.listen(command='sam spy')
@ensure_init
def spy(manager: SamManager, bot, message: SteelyMessage):
    manager.spy(bot, message)

@plugin.listen(command='sam treat')
@ensure_init
def treat(manager: SamManager, bot, message: SteelyMessage):
    manager.treat(bot, message)

@plugin.listen(command='sam scold')
@ensure_init
def scold(manager: SamManager, bot, message: SteelyMessage):
    manager.scold(bot, message)

@plugin.listen(command='sam kill')
@ensure_init
def kill(manager: SamManager, bot, message: SteelyMessage):
    manager.kill(bot, message)

@plugin.listen(command='sam [addressed]')
@ensure_init
def addressed(manager: SamManager, bot, message: SteelyMessage):
    manager.addressed(bot, message)

def test():
    # run some tests without using openai
    samdef = """
    @name Samara "Sam" Cabrera
    @bio Samara is a brilliant coder who grew up in a lower class neighborhood, honing her skills on old computers she fixed up herself.
    @age 26
    @location New York City, USA
    @bond Samara cares deeply about her little sister, who looks up to her as a role model.
    @flaw Samara can be overly critical of herself and others, leading to strained relationships.
    @trait Samara has an uncanny ability to spot bugs and errors in code, making her a master troubleshooter.
    @style Samara's texting style is quick and to the point, often using acronyms and tech lingo.
    @intro Hey everyone, it's Samara - ready to debug any code conundrums you throw my way!'>,)
    """
    ai = AI()
    p = ai.parse_samdef(AI.SAM_DEFAULT._asdict(), samdef)
    print(p)
    replaced = AI.SAM_DEFAULT._make(p.values())
    print(replaced)

