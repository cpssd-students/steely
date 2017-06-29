import random


COMMAND = '.8'
REPLIES = (
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don\'t count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(random.choice(REPLIES), thread_id=thread_id, thread_type=thread_type)
