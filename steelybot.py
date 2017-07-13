#!/usr/bin/env python3


from fbchat import log, Client
import imp
import threading
import config
import os
import sys
import random
import spell
from tinydb import TinyDB


CMD_DB = TinyDB('quote.json')


class SteelyBot(Client):

    def __init__(self, *args, **kwargs):
        super(SteelyBot, self).__init__(*args, **kwargs)
        self.last_suggestions = {}
        self.load_plugins()

    def load_plugins(self):
        self.non_plugins = []
        self.plugins = {}
        self.plugin_helps = {}
        for file in os.listdir('plugins'):
            if file.startswith("_"):
                continue
            elif not file.endswith(".py"):
                continue
            plugin_path = os.path.join('plugins', file)
            plugin = imp.load_source(file, plugin_path)
            if plugin.__doc__:
                self.plugin_helps[plugin.COMMAND.lower()] = plugin.__doc__
            if plugin.COMMAND:
                self.plugins[plugin.COMMAND.lower()] = plugin
            else:
                self.non_plugins.append(plugin)
        spell.WORDS = self.plugins.keys()

    def send_command(self, author_id, message, thread_id, thread_type, **kwargs):
        # run plugins that have a command
        if " " in message:
            command, message = message.split(' ', 1)
        else:
            command, message = message, ""
        command = command.lower()
        if not command in self.plugins:
            suggestions = list(enumerate(spell.correction(command)))
            if not suggestions:
                return
            if len(suggestions) == 1:
                command = suggestions[0][1]
            else:
                self.sendMessage('type the number to correct\n' +
                        ", ".join("{}: {}".format(n, suggestion) for n, suggestion in suggestions),
                        thread_id=thread_id, thread_type=thread_type)
                self.last_suggestions = suggestions
                self.last_message = message
                return
        plugin = self.plugins[command]
        thread = threading.Thread(target=plugin.main,
            args=(self, author_id, message, thread_id, thread_type), kwargs=kwargs)
        thread.deamon = True
        thread.start()

    def onEmojiChange(self, author_id, new_emoji, thread_id, thread_type, **kwargs):
        nose = '👃'
        if new_emoji != nose:
            self.changeThreadEmoji(nose, thread_id=thread_id)

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        if author_id == self.uid:
            return

        message_parts = message.split()
        if message_parts[0] in ('.list', '.help'):
            if len(message_parts) == 1:
                commands = ', '.join((command for command in self.plugins.keys() if command))
                user_cmds = ', '.join((command['cmd'] for command in CMD_DB))
                self.sendMessage('available commands: {}\nuser commands: {}'.format(commands, user_cmds),
                    thread_id=thread_id, thread_type=thread_type)
            else:
                plugin = message_parts[1]
                if not plugin.startswith("."):
                    plugin = "." + plugin
                if not plugin in self.plugin_helps:
                    self.sendMessage('help not found for command "{}"'.format(plugin),
                        thread_id=thread_id, thread_type=thread_type)
                    return
                self.sendMessage("```" + self.plugin_helps[plugin] + "```",
                    thread_type=thread_type, thread_id=thread_id)
            return

        if message == '.reload':
            self.load_plugins()
            self.sendMessage('plugins reloaded', thread_id=thread_id, thread_type=thread_type)
            return

        if message == '.restart':
            self.sendMessage('about to restart', thread_id=thread_id, thread_type=thread_type)
            os.execv(sys.executable, ['python'] + sys.argv)

        # run plugins that have no command
        for plugin in self.non_plugins:
                thread = threading.Thread(target=plugin.main,
                    args=(self, author_id, message, thread_id, thread_type), kwargs=kwargs)
                thread.deamon = True
                thread.start()

        if message.isdigit():
            for number, suggestion in self.last_suggestions:
                if number == int(message):
                    message = suggestion + " " + self.last_message
                    self.send_command(author_id, message, thread_id, thread_type, **kwargs)
                    self.last_message = ""
                    self.last_suggestions = []
                    return

        if not message.startswith("."):
            return

        self.send_command(author_id, message, thread_id, thread_type, **kwargs)


if __name__ == '__main__':
    client = SteelyBot(config.EMAIL, config.PASSWORD)
    client.listen()
