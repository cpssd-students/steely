from formatting import *
import config


__author__ = 'devoxel'
COMMAND = 'help'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    message_parts = message.split()
    if not message_parts:
        commands = ', '.join((config.COMMAND_PREFIX + command \
                              for command in bot.plugins.keys() \
                              if command))
        send_message(f'available commands: {commands}')
    else:
        plugin = message_parts[0]
        if plugin.startswith(config.COMMAND_PREFIX):
            plugin = plugin[1:]
        if not plugin in bot.plugin_helps:
            send_message(f'help not found for command {plugin!r}')
            return
        send_message(code_block(bot.plugin_helps[plugin]))
