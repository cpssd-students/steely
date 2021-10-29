from plugin import create_plugin
from message import SteelyMessage

plugin = create_plugin(name='b', author='byxor',
                       help='will transform the previous message into something a bit more exciting.')

REPLACEABLE = 'PpBbGg'
REPLACEMENT = '🅱️'

def encode(string):
    for sequence in REPLACEABLE:
        string = string.replace(sequence, REPLACEMENT)
    return string


@plugin.listen(command='b')
def b_listener(bot, message: SteelyMessage, **kwargs):
    text = bot.fetchThreadMessages(thread_id=message.thread_id, limit=2)[1].text
    bot.sendMessage(encode(text),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)
