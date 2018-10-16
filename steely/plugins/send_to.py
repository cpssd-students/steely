'''usage: .sendto [group|page|room|user] <thread_id> <message>'''


import requests
from steely import config
from fbchat import models


__author__ = 'sentriz'
COMMAND = 'sendto'
THREAD_TYPES = {
    'group': models.ThreadType.GROUP,
    'page':  models.ThreadType.PAGE,
    'room':  models.ThreadType.ROOM,
    'user':  models.ThreadType.USER
}

def parse_message(message):
    ''' returns (thread_type, thread_id, message)
    '''
    if ' ' not in message:
        return
    message_parts = message.split()
    if len(message_parts) < 3:
        return
    type_name = message_parts[0]
    if type_name not in THREAD_TYPES:
        return
    return THREAD_TYPES[type_name], message_parts[1], ' '.join(message_parts[2:])

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not author_id in ('100002084833976', '1640731564', '100000433265428'):
        send_message('sorry sam, only select people can use this command.')
        return
    message_parsed = parse_message(message)
    if not message_parsed:
        send_message('see help')
        return
    target_thread_type, target_thread_id, target_message = message_parsed
    bot.sendMessage(target_message, 
                    thread_id=target_thread_id,
                    thread_type=target_thread_type)
    send_message('sent')
