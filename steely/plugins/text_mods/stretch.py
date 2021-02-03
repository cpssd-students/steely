import random

from plugin import create_plugin
from message import SteelyMessage

plugin = create_plugin(name='stretch', author='CianLR',
                       help='gives the previous message sttrreeetttccchhhheeeeddddd')

STRETCH_FACTOR = 5


@plugin.listen(command='stretch')
def stretch(bot, trigger: SteelyMessage, **kwargs):
    message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
    if not message or not message.text:
        return
    if len(message.text) > 300:
        bot.sendMessage('Too long you spammy fuck',
                        thread_id=trigger.thread_id,
                        thread_type=trigger.thread_type)
        return
    out = ''
    count = 1
    for c in message.text:
        if random.random() < (STRETCH_FACTOR / len(message.text)):
            count += 1
        out += c * count
    bot.sendMessage(out,
                    thread_id=trigger.thread_id,
                    thread_type=trigger.thread_type)
