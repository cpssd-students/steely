COMMAND = '.b'
__author__ = ('byxor',)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    last_message = lambda: bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    send = lambda message: bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)

    send(encode(last_message()))

    
REPLACEABLE = [character for character in 'PpBbGg']
REPLACEMENT = '🅱️'
    

def encode(string):
    for sequence in REPLACEABLE:
        string = string.replace(sequence, REPLACEMENT)
    return string


def help():

    line_separated = lambda strings: "\n".join(strings)

    def code_block(contents):
        tag = "```"
        return tag + contents + tag
    
    return code_block(line_separated([
        COMMAND,
        encode("will transform the previous message into something a bit more exciting."),
    ]))


import sys
sys.modules[__name__].__doc__ = help()
