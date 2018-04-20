'''walklikeanegyptian'''

__author__ = 'iandioch'
COMMAND = 'egypt'

NORMAL = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
CURSED = '𓊏𓊐𓊑𓊒𓊓𓊔𓊕𓊖𓊗𓊘𓊙𓊚𓊛𓊜𓊝𓊞𓊟𓊠𓊡𓊢𓊣𓊤𓊥𓊦𓊧𓊨𓊩𓊪𓊫𓊬𓊭𓊮𓊯𓊰𓊱𓊲𓊳𓊴𓊵𓊶𓊷𓊸𓊹𓊺𓊻𓊼𓊽𓊾𓊿𓋀𓋁𓋂'
FROM = NORMAL + CURSED
TO = CURSED + NORMAL
TRANS = str.maketrans(FROM, TO)


def curse(text):
    return text.translate(TRANS)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(curse(message.text), thread_id=thread_id,
                    thread_type=thread_type)

if __name__ == '__main__':
    print(curse('The curse of the pharaohs refers to an alleged curse believed by some to be cast upon any person who disturbs the mummy of an Ancient Egyptian person, especially a pharaoh'))
    print(curse("𓊖𓊓𓊧𓊜𓊝𓊥𓊧𓊝𓊣'𓊠𓊓𓊏𓊜𓊏𓊚𓊚𓊡𓊢𓊏𓊠"))
