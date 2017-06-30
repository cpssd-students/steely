import random


COMMAND = '.8'
REPLIES = (
    "it is certain",
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
    "very doubtful"
)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(random.choice(REPLIES), thread_id=thread_id, thread_type=thread_type)
