'''predict the future with mersenne twister'''


import random


__author__ = 'sentriz'
COMMAND = '.8'
REPLIES = (
    "it is certain",
    "okay sam",
    "it is decidedly so",
    "without a doubt",
    "yes, definitely",
    "you may rely on it",
    "as i see it, yes",
    "most likely",
    "outlook good",
    "yes",
    "signs point to yes",
    "reply hazy, try again",
    "ask again later",
    "better not tell you now",
    "cannot predict now",
    "concentrate and ask again",
    "don\'t count on it",
    "my reply is no",
    "my sources say no",
    "outlook not so good",
    "very doubtful",
    "i have no idea",
)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(random.choice(REPLIES), thread_id=thread_id, thread_type=thread_type)
