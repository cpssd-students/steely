'''gives the previous command ａｅｓｔｈｅｔｉｃ'''


__author__ = ('alexkraak', 'sentriz')
COMMAND = '.vape'


import vapor


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(f"「{vapor.vapor(message.text)}", thread_id=thread_id, thread_type=thread_type)
