from plugin import create_plugin, PluginManager
from message import SteelyMessage

HELP_STR = """
Request your faviourite bible quotes, right to the chat.
"""

plugin = create_plugin(name='bible', author='CianLR', help=HELP_STR)


@plugin.setup()
def plugin_setup():
    pass


@plugin.listen(command='bible help')
def help_command(bot, message: SteelyMessage, **kwargs):
    pass


@plugin.listen(command='bible [passage]')
def passage_command(bot, message: SteelyMessage, **kwargs):
    pass
