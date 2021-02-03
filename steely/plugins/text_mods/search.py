import re

from plugin import create_plugin
from message import SteelyMessage


plugin = create_plugin(name='search',
        author='EdwardDowling',
        help='searches the previous message')


@plugin.listen(command='search')
def mock_listener(bot, trigger: SteelyMessage, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=trigger.thread_id, thread_type=trigger.thread_type)
    prev_message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
    match = re.findall(trigger.text, prev_message.text)[:10]
    if match:
        send_message('\n'.join(match))
    else:
        send_message('no match idiot')
