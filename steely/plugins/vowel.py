'''no'''
import random


__author__ = 'izaakf'
COMMAND = 'muck'


def shuffle(string):
    return ''.join(random.sample(string, len(string)))


def vowel_switch(string):
    vowels = "aeiou"
    normal = vowels + vowels.upper()
    shuffled = shuffle(vowels) + shuffle(vowels.upper())
    shuffle_trans = str.maketrans(normal, shuffled)
    return string.translate(shuffle_trans)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(vowel_switch(message.text),
                    thread_id=thread_id, thread_type=thread_type)
