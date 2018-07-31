'''to purge the naughtiness just incase'''


import shutil


__author__ = 'izaakf'
COMMAND = '.nuke'


PROBABLY_ENOUGH_TO_BAN_STEELY = 5000


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    for i in range(PROBABLY_ENOUGH_TO_BAN_STEELY):
        bot.sendMessage('goodnight sam', thread_id=thread_id, thread_type=thread_type)
    shutil.rmtree('../../steely')
