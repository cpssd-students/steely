'''It's not just a phase mom'''


__author__ = 'iandioch'
COMMAND = 'goth'


NORMAL = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
GOTH =   '𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ'
GOTH_TRANS = str.maketrans(NORMAL, GOTH)


def gothify(string):
    return string.translate(GOTH_TRANS)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(gothify(message.text), thread_id=thread_id, thread_type=thread_type)
