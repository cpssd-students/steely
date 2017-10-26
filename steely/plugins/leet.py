'''gives the previous command leet'''


__author__ = 'sentriz'
COMMAND = 'leet'
NORMAL = "abcdefghijklmnopqrstuvwxyz"
LEET =   "48(d3f9#|jklmn0pqr5+uvwxy2"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    last_message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    if message in ("undo", "u"):
        leet_trans = str.maketrans(LEET, NORMAL)
    else:
        leet_trans = str.maketrans(NORMAL, LEET)
    new_message = last_message.text.translate(leet_trans)
    bot.sendMessage(new_message, thread_id=thread_id, thread_type=thread_type)
