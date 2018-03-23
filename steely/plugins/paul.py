import re
from nltk.corpus import wordnet


__author__ = 'sentriz'
COMMAND = None
EXPRESSION = re.compile(r'^computer,\s+(\w+).*please(?:\.|\!)?$', \
                        re.DOTALL + \
                        re.IGNORECASE)
Y_RESPONSE = "Yes, Paul."
N_RESPONSE = "No, Paul."


def word_is_noun(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return False
    return synsets[0].pos() == "n"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    match = re.match(EXPRESSION, message)
    if not match:
        return
    first_word = match.group(1)
    if word_is_noun(first_word):
        bot.sendMessage(Y_RESPONSE, thread_id=thread_id, thread_type=thread_type)
    else:
        bot.sendMessage(N_RESPONSE, thread_id=thread_id, thread_type=thread_type)
