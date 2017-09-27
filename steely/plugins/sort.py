'''message -> aeegmss'''

__author__ = 'iandioch'
COMMAND = '.sort'


def sort_message(message):
    print(message)
    if not message:
        return ""
    out = ''.join(sorted(message))
    print(out)
    return out

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(sort_message(message.text), thread_id=thread_id, thread_type=thread_type)
