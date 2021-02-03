from plugin import create_plugin
from message import SteelyMessage


plugin = create_plugin(name='sort',
                       author='iandioch',
                       help='message -> aeegmss')


@plugin.listen(command='sort')
def mock_listener(bot, trigger: SteelyMessage, **kwargs):
    message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
    bot.sendMessage(''.join(sorted(message.text)),
                    thread_id=trigger.thread_id,
                    thread_type=trigger.thread_type)
