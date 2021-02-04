import random

from plugin import create_plugin
from message import SteelyMessage

plugin = create_plugin(name='scramble', author='izaakf',
        help='"hey add me on kik" -> "kik me add hey on"')

def scramble(message):
    split_message = message.split()
    if len(split_message) == 0:
        return ""
    elif len(split_message) > 250:
        return "You can't zucc me"
    random.shuffle(split_message)
    return " ".join(split_message)

@plugin.listen(command='scramble')
def listen(bot, messsage: SteelyMessage, **kwargs):
    message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
    bot.sendMessage(scramble(message.text),
            thread_id=trigger.thread_id,
            thread_type=trigger.thread_type)
