from formatting import *


__author__ = 'devoxel'
COMMAND = '.help'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message_parts = message.split()
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not message_parts:
        commands = ', '.join((command for command in bot.plugins.keys() if command))
        send_message(f'available commands: {commands}')
    else:
        plugin = message_parts[0]
        if not plugin.startswith("."):
            plugin = "." + plugin
        if not plugin in bot.plugin_helps:
            send_message(f'help not found for command {plugin!r}')
            return
        send_message(code_block(bot.plugin_helps[plugin]))
    return
