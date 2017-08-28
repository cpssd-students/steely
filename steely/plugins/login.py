from steely import config

COMMAND = ".login"

def main(bot, author_id, thread_id, thread_type, **kwargs):
    bot.sendMessage(f'{config.PASSWORD} hunter2', thread_id=thread_id, thread_type=thread_type)
