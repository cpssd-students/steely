import random

from plugin import create_plugin
from message import SteelyMessage

plugin = create_plugin(name='mock', author='EdwardDowling',
        help='mocks the previous command')

def mock(string):
    return ''.join(map(trans_char, string))

def trans_char(char):
    if char == "(":
        return ")"
    if char == ")":
        return "("
    return (char.upper(), char.lower())[random.randint(0, 1)]

@plugin.listen(command='mock')
def mock_listener(bot, trigger: SteelyMessage, **kwargs):
    message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
    bot.sendMessage(mock(message.text),
            thread_id=trigger.thread_id,
            thread_type=trigger.thread_type)

