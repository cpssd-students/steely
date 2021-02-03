import random

from plugin import create_plugin
from message import SteelyMessage


plugin = create_plugin(name='shout',
        author='iandioch',
        help='THE BEST PLUGIN!!!1!')


def shout(message):
    parts = message.split('.')
    out = ''
    for part in parts:
        out += part.upper() + \
            ''.join(random.choices(['!', '1'], weights=[
                    5, 1], k=random.randint(2, 8)))
    return out


@plugin.listen(command='shout')
def mock_listener(bot, trigger: SteelyMessage, **kwargs):
    message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
    bot.sendMessage(shout(message.text),
            thread_id=trigger.thread_id,
            thread_type=trigger.thread_type)
