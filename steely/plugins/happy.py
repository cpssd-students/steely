COMMAND = '.snack'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage('thanks!',
                    thread_id=thread_id, thread_type=thread_type)
