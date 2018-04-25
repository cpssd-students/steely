import random
from fbchat import MessageReaction, EmojiSize


__author__ = 'sentriz'
COMMAND = None


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = message.lower()
    if random.random() < 0.001:
        bot.sendEmoji("😠", EmojiSize.LARGE, thread_id, thread_type)
        return
    if any(word in message for word in ("tayne", "reed", "bot", "steely")) \
            and random.random() < 0.1:
        if random.random() < 0.7:
            bot.reactToMessage(kwargs['mid'], MessageReaction.ANGRY)
        else:
            bot.sendEmoji("😠", EmojiSize.LARGE, thread_id, thread_type)
    elif "cans" in message and random.random() < 0.1:
        bot.reactToMessage(kwargs['mid'], MessageReaction.LOVE)
