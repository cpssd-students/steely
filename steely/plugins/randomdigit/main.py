import random

from plugin import create_plugin
from message import SteelyMessage

HELP_STR = """
Requests steely to print a random digit to the chat.

Usage:
    /randomdigit - Requests a random digit
    /randomdigit help - This help text
"""

plugin = create_plugin(name='randomdigit', author='CianLR', help=HELP_STR)

SIDE = ['left', 'right']
DIGIT = [
    'big toe',
    'long toe',
    'middle toe',
    'ring toe',
    'little toe',
    'thumb',
    'index finger',
    'middle finger',
    'ring finger',
    'pinky',
]

@plugin.setup()
def plugin_setup():
    pass

@plugin.listen(command='randomdigit help')
def help_command(bot, message: SteelyMessage, **kwargs):
    bot.sendMessage(
            HELP_STR,
            thread_id=message.thread_id, thread_type=message.thread_type)

@plugin.listen(command='randomdigit')
def choose_command(bot, message: SteelyMessage, **kwargs):
    the_chosen_one = random.choice(SIDE) + ' ' + random.choice(DIGIT)
    bot.sendMessage(
            the_chosen_one.capitalize(),
            thread_id=message.thread_id, thread_type=message.thread_type)

