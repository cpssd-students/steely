from plugin import create_plugin, PluginManager

plugin = create_plugin(name='nw', author='iandioch', help='todo')

@plugin.setup()
def plugin_setup():
    # TODO(iandioch): Set up/load a DB of registered usernames.
    return

@plugin.listen(command='nw')
def root_command(bot, author_id, message, thread_id, thread_type, **kwargs):
    print(author_id, message)

@plugin.listen(command='nw help')
def help_command(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(plugin.help, thread_id=thread_id, thread_type=thread_type)


nw_command = PluginManager.get_listener_for_command('nw')
if nw_command:
    print('running "/nw"')
    nw_command(None, 1234, 'message', 5678, 91011)
else:
    print('no command found for "/nw"')
