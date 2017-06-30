import random
from fbchat import MessageReaction


COMMAND = None


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if random.random() < 0.05:
        bot.reactToMessage(kwargs['mid'], MessageReaction.ANGRY)
