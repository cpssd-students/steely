'''
Flip a coin with .coinflip

You'll either get heads or tails, and an interesting message along with it.
'''


import random


__author__ = ('alexkraak', 'byxor')
COMMAND = 'coinflip'


PREFIXES = ("good egg", "ok sam", "incredible", "aaaaaaaaaand", "ouch",
            "damn son", "go on my son", "what a flip",
            "that was a fucking disgrace",
            "well spread some peanut butter on my asshole and call me michelle")
MIDDLES =  ("you got", "you landed on", "you managed to flip it onto",
            "looks like you got", "you bagged yourself")
SUFFIXES = ("better luck next time", "that was pretty good",
            "i never want to play this game again", "kill me please",
            "i wonder if linden has been fixed yet",
            "can i have a snack now?")
PROBABILITY_OF_SUFFIX = 0.1


IMAGES = {'heads': 'https://www.random.org/coins/faces/60-eur/ireland-1euro/reverse.jpg',
          'tails': 'https://www.random.org/coins/faces/60-eur/ireland-1euro/obverse.jpg'}


def coinflip():
    PROBABILITY_OF_COIN_RESULT = 0.5
    return "heads" if _chance(PROBABILITY_OF_COIN_RESULT) else "tails"


def generate_speech_for(result):
    prefix = random.choice(PREFIXES)
    middle = random.choice(MIDDLES)
    speech = f"{prefix}, {middle} {result}!"
    if _chance(PROBABILITY_OF_SUFFIX):
        suffix = random.choice(SUFFIXES)
        speech += f" {suffix}"
    return speech


def _chance(probability_of_success):
    return random.random() < probability_of_success


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    flip = coinflip()
    speech = generate_speech_for(flip)
    image = IMAGES[flip]
    bot.sendRemoteImage(image,
        thread_id=thread_id, thread_type=thread_type)
    bot.sendMessage(speech,
        thread_id=thread_id, thread_type=thread_type)
