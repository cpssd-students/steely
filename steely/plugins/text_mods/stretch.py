import random

from plugin import create_plugin
from message import SteelyMessage

plugin = create_plugin(name='stretch', author='CianLR',
        help='gives the previous message sttrreeetttccchhhheeeeddddd')

STRETCH_FACTOR = 5


@plugin.listen(command='stretch')
def stretch(bot, message: SteelyMessage, **kwargs):
    if not message or not message.text:
        return
    if len(message.text) > 300:
        bot.sendMessage('Too long you spammy fuck',
                thread_id=message.thread_id,
                thread_type=message.thread_type)
        return
    out = ''
    count = 1
    for c in message:
        if random.random() < (STRETCH_FACTOR / len(message.text)):
            count += 1
        out += c * count
    bot.sendMessage(out,
            thread_id=message.thread_id,
            thread_type=message.thread_type)
