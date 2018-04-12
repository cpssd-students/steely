'''dont use this'''


import requests
from steely import config


__author__ = 'sentriz'
COMMAND = 'sendtocachat'
CA_CHAT_ID = '1182752481782139'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not message.strip():
        send_message('nice try idiot')
        return
    if not author_id in ('100002084833976', '1640731564', '100000433265428'):
        send_message('sorry sam, only select people can use this command.\n'
                     'we couldnt want poor reed getting removed from the ca chat would we?')
        return
    bot.sendMessage(message, thread_id=CA_CHAT_ID, thread_type=thread_type)
    send_message('sent')
