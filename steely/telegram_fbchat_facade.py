from telegram.ext import Updater, MessageHandler
from telegram.ext.filters import Filters

class Client:
    '''Acts as a facade on fbchat bots to allow them to be backed by Telegram
    instead. ie., Provides API compatibility.'''

    def __init__(self, email, password):
        '''Creates a client.

        Args:
            email (str): Is thrown away.
            password (str): Is used as the Telegram bot key.'''
        self.updater = Updater(token=password)
        self.dispatcher = self.updater.dispatcher
        self.uid = self.updater.bot.username

    def listen(self):
        def innerOnMessage(bot, update):
            try:
                print(update.message)
                self.onMessage(author_id=update.effective_user.id,
                               message=update.effective_message.text,
                               thread_id=update.effective_chat.id,
                               thread_type=update.effective_chat.type)
            except Exception as e:
                log(e)
        self.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=innerOnMessage))
        self.updater.start_polling()
        self.updater.idle()

    def markAsDelivered(self, *args, **kwargs):
        '''TODO: Remove this method, it's only here to suppress errors.'''
        pass

    def markAsRead(self, *args, **kwargs):
        '''TODO: Remove this method, it's only here to suppress errors.'''
        pass

    def onEmojiChange(self, author_id, new_emoji, thread_id, thread_type, **kwargs):
        '''Handler method; to be overriden.'''
        pass

    def onNicknameChange(self, mid, author_id, changed_for, new_nickname, thread_id, thread_type, ts, metadata, msg):
        '''Handler method; to be overriden.'''
        pass

    def onFriendRequest(self, from_id, msg):
        '''Handler method; to be overriden.'''
        pass

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        '''Handler method; to be overriden.'''
        pass

def log(*args, **kwargs):
    print("log:", *args, *kwargs)