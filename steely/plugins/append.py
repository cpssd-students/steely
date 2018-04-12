'''append some text to some other text'''

__author__ = 'devoxel'
COMMAND = 'append'


def appendify(s, to_append):
    o = s + to_append
    if len(o) > 300:
        return "a dollop of spam"
    return o


def main(bot, author_id, to_append, thread_id, thread_type, **kwargs):
    last_message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(appendify(last_message.text, to_append),
                    thread_id=thread_id, thread_type=thread_type)
