from collections import defaultdict, deque
from enum import Enum

from telegram.ext import Updater, MessageHandler
from telegram.ext.filters import Filters

ThreadType = Enum('ThreadType', 'USER GROUP')

def _telegram_chat_to_fbchat_thread_type(chat):
    # TODO(iandioch): Figure out what a supergroup is.
    if chat.type == 'private':
        return ThreadType.USER
    return ThreadType.GROUP

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
        self.bot = self.updater.bot
        self.uid = self.updater.bot.username

        self.thread = defaultdict(lambda: deque(iterable=[], maxlen=16))

    def listen(self):
        def innerOnMessage(bot, update):
            try:
                print(update.message)
                thread_id = update.effective_chat.id
                thread_type = _telegram_chat_to_fbchat_thread_type(
                        update.effective_chat)
                self.thread[thread_id].append(update.effective_message)
                self.onMessage(author_id=update.effective_user.id,
                               message=update.effective_message.text,
                               thread_id=thread_id,
                               thread_type=thread_type)
            except Exception as e:
                log(e)
        self.dispatcher.add_handler(MessageHandler(filters=Filters.all,
                                                   callback=innerOnMessage))
        self.updater.start_polling()
        self.updater.idle()

    def fetchThreadMessages(self, thread_id, limit):
        # TODO(iandioch): Support different threads.
        # TODO(iandioch): Do this more efficiently than list()
        return list(self.thread[thread_id])[::-1][:limit]

    def sendMessage(self, text, thread_id, thread_type):
        '''Sends a message.

        Args:
            text (str): The message to send.
            thread_id (str): The chat id to send the message to.
            thread_type (str): Is thrown away.'''
        self.bot.sendMessage(chat_id=thread_id, text=text)

    def sendRemoteImage(self, image, thread_id, thread_type):
        # TODO(iandioch): this.
        print('Trying to send image {}'.format(image))
        try:
            self.bot.sendPhoto(chat_id=thread_id,
                               photo=image)
        except Exception as e:
            log(e)

    def markAsDelivered(self, *args, **kwargs):
        '''TODO: Remove this method, it's only here to suppress errors.'''
        pass

    def markAsRead(self, *args, **kwargs):
        '''TODO: Remove this method, it's only here to suppress errors.'''
        pass

    def onEmojiChange(self, author_id, new_emoji,
                      thread_id, thread_type, **kwargs):
        '''Handler method; to be overriden.'''
        pass

    def onNicknameChange(self, mid, author_id, changed_for, new_nickname,
                         thread_id, thread_type, ts, metadata, msg):
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
