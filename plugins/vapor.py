COMMAND = '.vapor'

def vapor(string):
    return ' '.join(string)

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(vapor(message.text), thread_id=thread_id, thread_type=thread_type)
