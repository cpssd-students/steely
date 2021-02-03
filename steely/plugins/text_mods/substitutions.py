# File to configure simple substitution plugins, like /goth, /bubble, etc.,
# which just translate the alphabet [a-zA-Z] to some equivalents in another
# script.

from plugin import create_plugin
from message import SteelyMessage

# Helper method to create a plugin that just translates the alphabet.
def create_substitution_plugin(command, author, help, trans):
    NORMAL = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    TRANS = str.maketrans(NORMAL, trans)

    plugin = create_plugin(name=command, author=author, help=help)
    @plugin.listen(command=command)
    def plugin_listener(bot, trigger: SteelyMessage, **kwargs):
        message = bot.fetchThreadMessages(thread_id=trigger.thread_id, limit=2)[1]
        text = message.text.translate(TRANS)
        bot.sendMessage(text,
                thread_id=trigger.thread_id,
                thread_type=trigger.thread_type)

create_substitution_plugin('goth', 'iandioch', 'It\'s not just a phase mom',
        '𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ')
