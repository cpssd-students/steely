#!/usr/bin/env python3
'''
.define [`code`] <command_name> <some text ...>

.define allows you to add commands which contains text.
They can be accessed via ~<command_name>, and will output what you put in.

.define code <text> will format the input as code.
'''


from tinydb import TinyDB, Query


COMMAND = '.define'
CMD_DB = TinyDB('quote.json')
CMD = Query()
# if u guess the correct expression used to generate LIMIT
# i will give u a biscuit
LIMIT = 8234

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if len(message) > LIMIT:
        bot.sendMessage('thats too long dickhead', thread_id=thread_id, thread_type=thread_type)
    message_split = message.split()
    if message_split[0] == 'code' and len(message_split) >= 3:
        # this might seem hacky, but you're wrong
        # adding a single ``` works because facebook is weird
        message_split = message_split[1] + ['```\n'] + message_split[2:] 
    search = CMD_DB.get(CMD.cmd == '~' + message_split[0])
    if len(message_split) >= 2:
        if search == None:
            CMD_DB.insert({"cmd": '~' + message_split[0],
                           "text": " ".join(message_split[1:])})
            bot.sendMessage('Your command can be run with ~' + message_split[0],
                            thread_id=thread_id, thread_type=thread_type)
            return
        else:
            CMD_DB.update({"text": " ".join(message_split[1:])}, CMD.cmd == '~' + message_split[0])
            bot.sendMessage('Your command ~{} has been updated'.format(message_split[0]),
                            thread_id=thread_id, thread_type=thread_type)
            return

    else:
        bot.sendMessage('please use in form .define <command_name> <command text>',
                        thread_id=thread_id, thread_type=thread_type)
        return
