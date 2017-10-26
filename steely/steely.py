#!/usr/bin/env python3


from contextlib import suppress
from fbchat import log, Client
from tinydb import TinyDB
from vapor import vapor
from utils import list_plugins
import config
import imp
import os
import random
import requests
import sys
import threading


HELP_DOC = '''help <command>

help syntax:
optinal arguments: [arg name]
mandatory arguments: <arg name>
literal arguments: `this|yesterday|tomorrow`

literal commands can be mandatory or optional'''


class SteelyBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_suggestions = {}
        self.load_plugins()

    def load_plugins(self):
        self.non_plugins = []
        self.plugins = {}
        self.plugin_helps = {
            '.help': HELP_DOC
        }
        for plugin in list_plugins():
            if plugin.__doc__ and plugin.COMMAND:
                self.plugin_helps[plugin.COMMAND.lower()] = plugin.__doc__.strip('\n')
            if plugin.COMMAND:
                self.plugins[plugin.COMMAND.lower()] = plugin
            else:
                self.non_plugins.append(plugin)

    @staticmethod
    def parse_command_message(message):
        if message[0] != config.COMMAND_PREFIX:
            return
        command, _, message = message[1:].partition(' ')
        clean_command = command.lower().strip()
        return clean_command, message

    def run_plugin(self, author_id, message, thread_id, thread_type, **kwargs):
        parsed_message = self.parse_command_message(message)
        if parsed_message is None:
            return
        command, message = parsed_message
        if not command in self.plugins:
            return
        plugin = self.plugins[command]
        thread = threading.Thread(target=plugin.main,
            args=(self, author_id, message, thread_id, thread_type), kwargs=kwargs)
        thread.deamon = True
        thread.start()

    def run_non_plugins(self, author_id, message, thread_id, thread_type, **kwargs):
        for plugin in self.non_plugins:
            thread = threading.Thread(target=plugin.main,
                args=(self, author_id, message, thread_id, thread_type), kwargs=kwargs)
            thread.deamon = True
            thread.start()

    def onEmojiChange(self, author_id, new_emoji, thread_id, thread_type, **kwargs):
        nose = '👃'
        if new_emoji != nose:
            self.changeThreadEmoji(nose, thread_id=thread_id)

    def onNicknameChange(self, mid, author_id, changed_for, new_nickname, thread_id, thread_type, ts, metadata, msg):
        self.changeNickname(vapor(new_nickname), user_id=changed_for, thread_id=thread_id, thread_type=thread_type)

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)
        if author_id == self.uid:
            return
        self.run_non_plugins(author_id, message, thread_id, thread_type, **kwargs)
        self.run_plugin(author_id, message, thread_id, thread_type, **kwargs)


if __name__ == '__main__':
    client = SteelyBot(config.EMAIL, config.PASSWORD)
    while True:
        with suppress(requests.exceptions.ConnectionError):
            client.listen()
