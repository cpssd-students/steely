import hashlib
from steely import config


__author__ = "izaakf"
COMMAND = ".login"


def md5_of(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def main(bot, author_id, thread_id, thread_type, **kwargs):
    bot.sendMessage(f"{config.EMAIL} {md5_of(config.PASSWORD)}", 
        thread_id=thread_id, thread_type=thread_type)
