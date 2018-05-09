"""
OwO whats this?
"""

__author__ = ('Smurphicus')
COMMAND = 'owo'

from random import choice

substitutions = {'r':'w','R':'W','l':'w','L':'W','na':'nya','NA':'NYA','qu':'qw','QU':'QW'}
faces = [' OwO', ' owo', ' UwU', ' uwu', ' :3', ' :33', ' :333', '']

def owoify(message):
    for key in substitutions.keys():
        message = message.replace(key,substitutions[key])
    return message + choice(faces)

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    owoified_message = owoify(message.text)
    bot.sendMessage(owoified_message, thread_id=thread_id, thread_type=thread_type)
