import random

from plugin import create_plugin
from message import SteelyMessage


plugin = create_plugin(name='vowel', author='izaakf', help='no')


def shuffle(string):
    return ''.join(random.sample(string, len(string)))


def vowel_switch(string):
    vowels = "aeiou"
    normal = vowels + vowels.upper()
    shuffled = shuffle(vowels) + shuffle(vowels.upper())
    shuffle_trans = str.maketrans(normal, shuffled)
    return string.translate(shuffle_trans)


@plugin.listen(command='muck')
def mock_listener(bot, trigger: SteelyMessage, **kwargs):
    message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
    bot.sendMessage(vowel_switch(message.text),
                    thread_id=trigger.thread_id,
                    thread_type=trigger.thread_type)
