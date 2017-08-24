from plugins._lastfm_helpers import *


def main(bot, author_id, message_parts, thread_id, thread_type, **kwargs):
    if not message_parts:
        bot.sendMessage('provide a username',
                thread_id=thread_id, thread_type=thread_type)
        return
    username = message_parts[0]
    if not USERDB.search(USER.id == author_id):
        USERDB.insert({'id': author_id, 'username': username})
        bot.sendMessage('good egg', thread_id=thread_id, thread_type=thread_type)
    else:
        USERDB.update({'username': username}, USER.id == author_id)
        bot.sendMessage('updated egg', thread_id=thread_id, thread_type=thread_type)
