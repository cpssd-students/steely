'''reload all user plugins'''


COMMAND = '.reload'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.load_plugins()
    bot.sendMessage('plugins reloaded', thread_id=thread_id, thread_type=thread_type)
