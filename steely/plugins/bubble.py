'''ⓐyy lmao'''

__author__ = 'CianLR'
COMMAND = '.bubble'
NORMAL = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BUBBLED = 'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ'
TRANS = str.maketrans(NORMAL, BUBBLED)


def bubble(message):
    return message.translate(TRANS)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(bubble(message.text),
                    thread_id=thread_id,
                    thread_type=thread_type)


if __name__ == '__main__':
    print(bubble('Hi mom!'))
    print(bubble('I hate SAM'))
