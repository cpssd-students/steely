from steely import config

COMMAND = ".login"

def main(bot, author_id, thread_id, thread_type, **kwargs):
    bot.sendMessage(config.EMAIL, config.PASSWORD, thread_id=thread_id, thread_type=thread_type)
