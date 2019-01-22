'''reload all user plugins'''


from paths import CONFIG


__author__ = 'sentriz'
COMMAND = 'reload'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not author_id in CONFIG.ADMINS:
        send_message('no')
        return
    bot.load_plugins()
    send_message('plugins reloaded')
