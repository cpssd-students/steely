#!/usr/bin/env python3
"""
Haiku:
    A poem with 5 syllables on the first line,
    7 on the second
    and 5 on the third

    ...plus some other rules

This reads in all messages and prints out ones that accidentally fit the
definition of a haiku.
"""


from textstat.textstat import textstat  # wat

__author__ = 'CianLR'
COMMAND = None


def split_by_syllables(syls, words):
    s_count = 0
    split = 0
    while s_count < syls and split < len(words):
        s_count += round(textstat.syllable_count(words[split]))
        split += 1
    if s_count != syls:
        raise ValueError("Words do not evenly split")
    return words[:split], words[split:]


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if len(message.split()) > 17:
        return

    try:
        words = message.split()
        first, rest = split_by_syllables(5, words)
        middle, rest = split_by_syllables(7, rest)
        last, rest = split_by_syllables(5, rest)
        if rest:
            return
        bot.sendMessage(
                '\n'.join(map(' '.join, (first, middle, last))),
                thread_id=thread_id,
                thread_type=thread_type)
    except ValueError:
        pass


if __name__ == '__main__':
    class FakeBot:
        def sendMessage(self, message, *args, **kwargs):
            print(message)
    def main_wrapper(message):
        return main(FakeBot(), 123, message, 123, 123)

    main_wrapper("""
    I am first with five
    Then seven in the middle --
    Five again to end.""")

    main_wrapper("Hello sam my friend, it has been a long time boy, "
                 "I do miss your spam")

    main_wrapper("""
    Snowman in a field
    listening to the raindrops
    wishing him farewell""")
    
    main_wrapper("Oi mate are you avin a laf?")

    main_wrapper("hello there " * 100)

