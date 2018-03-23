'''reload all user plugins'''


import os
import sys
import config


__author__ = 'sentriz'
COMMAND = 'restart'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not author_id in config.ADMINS:
        send_message('no')
        return
    send_message('about to restart')
    os.execv(sys.executable, ['python'] + sys.argv)
