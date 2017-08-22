'''reload all user plugins'''


COMMAND = '.restart'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage('about to restart', thread_id=thread_id, thread_type=thread_type)
    os.execv(sys.executable, ['python'] + sys.argv)
