from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from formatting import *
from utils import new_database
from plugin import create_plugin 
from plugins.intern.db import *
from plugins.intern import simulation

HELP_STR = """
"""
plugin = create_plugin(name='intern', author='iandioch', help=HELP_STR)

@plugin.setup()
def setup():
    setup_database()

@plugin.listen(command='intern hire [intern_id]')
def hire(bot, message, **kwargs):
    if 'intern_id' in kwargs and kwargs['intern_id'] != '':
        intern_id = kwargs['intern_id']
        intern_ = get_intern(intern_id)
        hirer = bot.fetchUserInfo(message.author_id)[0]
        bot.sendMessage('{} is hiring intern {}.'.format(hirer['full_name'],
                                                         intern_.name),
                        thread_id=message.thread_id,
                        thread_type=message.thread_type)
        if intern_.manager is not None:
            bot.sendMessage('{} is already hired!'.format(intern_.name),
                            thread_id=message.thread_id,
                            thread_type=message.thread_type)
            return
        if get_intern_for_manager(message.author_id) is not None:
            bot.sendMessage('{} already has an intern!'.format(
                                hirer['first_name']),
                            thread_id=message.thread_id,
                            thread_type=message.thread_type)
            return
        intern_.manager = message.author_id
        update_intern(intern_)
        return

    unhired_interns = get_unhired_interns()
    intern_detail_strs = []
    button_list = []
    for unhired in unhired_interns:
        # Creates a button saying "Hire XYZ", that will send a command of the
        # form '/intern hire {intern_id}' when clicked.
        callback_data = '/intern hire {}'.format(unhired.id_)
        button_list.append([
            InlineKeyboardButton('Hire {}'.format(unhired.name),
                                 callback_data=callback_data)
        ])
        intern_detail_strs.append(render_intern_info(unhired))

    reply_markup = InlineKeyboardMarkup(button_list, n_cols=1)
    bot.sendMessage('\n---\n'.join(intern_detail_strs),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type,
                    reply_markup=reply_markup)

@plugin.listen(command='intern check')
def check(bot, message, **kwargs):
    intern_ = get_intern_for_manager(message.author_id)
    if intern_ is None:
        hire_button = InlineKeyboardButton('Hire an intern now',
                                           callback_data='/intern hire')
        reply_markup = InlineKeyboardMarkup([[hire_button]], n_cols=1)
        manager_info = bot.fetchUserInfo(message.author_id)[0]
        bot.sendMessage('{} has no intern!'.format(manager_info['full_name']),
                        thread_id=thread_id,
                        thread_type=thread_type,
                        reply_markup=reply_markup)
        return

    bot.sendMessage(render_intern_info(intern_),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)
    bot.sendMessage(simulation.check(intern_),
                    thread_id=message.thread_id,
                    thread_type=message.thread_type)
