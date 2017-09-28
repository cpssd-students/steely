'''gives the previous command leet'''


__author__ = 'sentriz'
COMMAND = '.leet'


def leet(string):
    normal = "abcdefghijklmnopqrstuvwxyz"
    leet =   "48(d3f9#|jklmn0pqr5+uvwxy2"
    leet_trans = str.maketrans(normal, leet)
    return string.translate(leet_trans)

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(leet(message.text), thread_id=thread_id, thread_type=thread_type)
