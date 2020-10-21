#!/usr/bin/env python3


from contextlib import suppress
from telegram_fbchat_facade import log, Client
from tinydb import TinyDB
from vapor import vapor
from utils import list_plugins
from plugin import PluginManager
from message import SteelyMessage
import config
import imp
import os
import random
import requests
import sys
import threading
import logging


HELP_DOC = '''help <command>

help syntax:
optinal arguments: [arg name]
mandatory arguments: <arg name>
literal arguments: `this|yesterday|tomorrow`

literal commands can be mandatory or optional'''


class SteelyBot(Client):
    '''Wraps around the Telegram Fbchat facade and handles Steely-specific stuff,
    ie. plugins.'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_suggestions = {}
        self.load_plugins()

    def load_plugins(self):
        PluginManager.load_plugins()
        self.non_plugins = []
        self.plugins = {}
        self.plugin_helps = {
            'help': HELP_DOC
        }
        for plugin in list_plugins():
            if plugin.__doc__ and plugin.COMMAND:
                self.plugin_helps[
                    plugin.COMMAND.lower()] = plugin.__doc__.strip('\n')
            if plugin.COMMAND:
                self.plugins[plugin.COMMAND.lower()] = plugin
            else:
                self.non_plugins.append(plugin)

    @staticmethod
    def parse_command_message(message):
        if not message:
            return
        if message[0] != config.COMMAND_PREFIX:
            return
        command, _, message = message[1:].partition(' ')
        clean_command = command.split('@')[0].lower().strip()
        return clean_command, message

    def run_plugin(self, author_id, message, thread_id, thread_type, **kwargs):
        parsed_message = self.parse_command_message(message)
        if parsed_message is None:
            return
        command, message = parsed_message

        # Run plugins following SEP1 interface.
        full_message = '{} {}'.format(command, message)
        matched_command, plugin, args = PluginManager.get_listener_for_command(full_message)
        if matched_command is not None:
            passed_kwargs = kwargs.copy()
            passed_kwargs.update(args)
            thread = threading.Thread(target=plugin,
                    args=(self, author_id, full_message[len(matched_command)+1:], thread_id, thread_type), kwargs=passed_kwargs)
            thread.deamon = True
            thread.start()

        # Run normal traditional steely plugins.
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

        for plugin in PluginManager.get_passive_listeners():
            thread = threading.Thread(target=plugin,
                                      args=(self, author_id, message, thread_id, thread_type), kwargs=kwargs)
            thread.deamon = True
            thread.start()


    def onMessage(self, message: SteelyMessage):
        if message.author_id == self.uid:
            return
        if message.text is None or message.text == '':
            # May occur when an image or sticker is sent.
            return
        self.run_non_plugins(message.author_id, message.text, message.thread_id,
                             message.thread_type)
        self.run_plugin(message.author_id, message.text, message.thread_id,
                        message.thread_type)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = SteelyBot(config.EMAIL, config.TELEGRAM_KEY)
    while True:
        with suppress(requests.exceptions.ConnectionError):
            client.listen()
