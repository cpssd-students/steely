'''gives the previous command ａｅｓｔｈｅｔｉｃ'''


__author__ = ('alexkraak', 'sentriz')
COMMAND = 'vape'


import vapor


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    vaped_message = vapor.vapor(message.text)
    bot.sendMessage(f"「{vaped_message}」", thread_id=thread_id, thread_type=thread_type)
