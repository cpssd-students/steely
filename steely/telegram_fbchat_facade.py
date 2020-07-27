import json
from collections import defaultdict, deque
from enum import Enum

from utils import new_database

from tinydb import Query
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler
from telegram.ext.filters import Filters

ThreadType = Enum('ThreadType', 'USER GROUP')

def _telegram_chat_to_fbchat_thread_type(chat):
    # TODO(iandioch): Figure out what a supergroup is.
    if chat.type == 'private':
        return ThreadType.USER
    return ThreadType.GROUP

class SteelyUserManager:
    '''Telegram doesn't allow any querying of users in a group, so we have to
    track user IDs ourselves if we want to be able to query them later.'''

    def __init__(self, user_db_path, thread_db_path):
        self.user_db = new_database(user_db_path)
        self.thread_db = new_database(thread_db_path)

    def _add_user_to_thread(self, thread_id, user_id):
        # TODO(iandioch): This data will be stale as soon as someone leaves a
        # group. We need a _delete_user_from_thread...
        THREAD = Query()
        threads = self.thread_db.search(THREAD.id == thread_id) 
        thread_data = {
                'id': thread_id,
        }
        if len(threads) == 0:
            thread_data['users'] = [user_id]
        else:
            # TODO(iandioch): This is inefficient af. Do it better (eg. query
            # "user_id not in users" at TinyDB level, instead of in python.
            thread_data['users'] = threads[0]['users']
            if user_id not in thread_data['users']:
                thread_data['users'].append(user_id)
        self.thread_db.upsert(thread_data, THREAD.id == thread_id)

    def maybe_add_user(self, bot, thread_id, user_id):
        '''Inform about an interaction with a user user_id in the given thread.
        It is required to add the thread because Telegram doesn't allow shot-in-
        the-dark queries about a given user ID.'''
        print('SteelyUserManager: Maybe adding user',
              user_id, 'in thread', thread_id)
        self._add_user_to_thread(thread_id, user_id)

        try:
            user_data = bot.get_chat_member(chat_id=thread_id, user_id=user_id)
        except Exception as e:
            print(e)
            return
        info = user_data.user
        data = {
            'id': user_id,
            'first_name': info.first_name, # eg. 'Noah'
            'last_name': info.last_name, # eg. 'Ó D'. Optional.
            'full_name': info.full_name, # eg 'Noah Ó D'
            'username': info.username, # eg. 'iandioch'
        }
        self.user_db.insert(data)

    def get_user_info(self, user_id):
        print('SteelyUserManager: requested user info', user_id)
        USER = Query()
        return self.user_db.search(USER.id == user_id)

    def get_thread_info(self, thread_id):
        print('SteelyUserManager: requested thread info', thread_id)
        THREAD = Query()
        return self.thread_db.search(THREAD.id == thread_id)

    def search_for_users(self, name): 
        print('SteelyUserManager: searching for user:', name)
        # TODO(iandioch): Find a closest user from the DB for full_name ~= name.
        return []


class Client:
    '''Acts as a facade on fbchat-alike bots to allow them to be backed by
    Telegram instead. ie., Provides API compatibility.'''

    NUM_STORED_MESSAGES_IN_THREAD = 16

    def __init__(self, email, password):
        '''Creates a client.

        Args:
            email (str): Is thrown away.
            password (str): Is used as the Telegram bot key.'''

        self.user_manager = SteelyUserManager(user_db_path='users',
                                              thread_db_path='threads')
        self.updater = Updater(token=password)
        self.dispatcher = self.updater.dispatcher
        self.bot = self.updater.bot
        self.uid = self.updater.bot.username

        # Each self.thread[thread_id] is a deque (FIFO linked list).
        self.thread = defaultdict(lambda: deque(iterable=[],
            maxlen=Client.NUM_STORED_MESSAGES_IN_THREAD))

    def listen(self):
        def innerOnMessage(bot, update):
            try:
                print(update.message)
                thread_id = update.effective_chat.id
                thread_type = _telegram_chat_to_fbchat_thread_type(
                        update.effective_chat)
                self.thread[thread_id].append(update.effective_message)
                author_id = update.effective_user.id
                self.user_manager.maybe_add_user(self.bot, thread_id, author_id)
                self.onMessage(author_id=author_id,
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
        # TODO(iandioch): Do this more efficiently than list()
        return list(self.thread[thread_id])[::-1][:limit]

    def sendMessage(self, text, thread_id, thread_type):
        '''Sends a message.

        Args:
            text (str): The message to send.
            thread_id (str): The chat id to send the message to.
            thread_type (str): Is thrown away.'''
        sent_message = self.bot.send_message(chat_id=thread_id, text=text,
                                             parse_mode=ParseMode.MARKDOWN)
        # Add steely's response to the log so you can mock him, etc.
        self.thread[thread_id].append(sent_message)

    def sendRemoteImage(self, image, thread_id, thread_type):
        '''Sends an image.

        Args:
            image (str): The URL of the image to send.
            thread_id (str): The chat id to send the message to.
            thread_type (str): Is thrown away.'''
        print('Trying to send image {}'.format(image))
        try:
            self.bot.sendPhoto(chat_id=thread_id,
                               photo=image)
        except Exception as e:
            log(e)

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        '''Handler method; to be overriden.'''
        pass

    def fetchUserInfo(self, user_id):
        '''Gets info about the given user(s).'''
        print('fetchUserInfo({})'.format(user_id))
        return self.user_manager.get_user_info(user_id)

    def fetchGroupInfo(self, thread_id):
        '''Gets info about the given group(s).'''
        print('fetchGroupInfo({})'.format(thread_id))
        return self.user_manager.get_thread_info(thread_id)

    def searchForUsers(self, name, limit=10):
        '''Finds users by their display name.'''
        return self.user_manager.search_for_users(name)

def log(*args, **kwargs):
    print("log:", *args, *kwargs)
