'''🆒'''

import random
import requests
from collections import defaultdict

__author__ = ('iandioch')
COMMAND = 'emoji'

EMOJI_DATA = {}
try:
    EMOJI_DATA = requests.get(
        'https://raw.githubusercontent.com/muan/emojilib/4cee8ed17f697b8a5a2e55d8d588ba0d9ce46c4c/emojis.json').json()
except Exception as e:
    print('No emoji data for you sir! Good day!')
    print(e)

# Feel free to add offensive or american words here.
BLACKLIST = set([
])

WORD_TO_EMOJI = defaultdict(list)

for k in EMOJI_DATA:
    if 'keywords' not in EMOJI_DATA[k]:
        continue
    emoji = EMOJI_DATA[k]['char']
    if emoji is None:
        continue

    # Without this if check, 'it' stil maps to an italian flag.
    if not (len(k) == 2 and EMOJI_DATA[k]['category'] == 'flags'):
        WORD_TO_EMOJI[k].append(emoji)
    
    for word in EMOJI_DATA[k]['keywords']:
        if word in BLACKLIST:
            continue
        if len(word) == 2 and EMOJI_DATA[k]['category'] == 'flags':
            continue
        WORD_TO_EMOJI[word].append(emoji)


def emojify_or_not_i_am_a_function_not_a_cop(word):
    w = word.lower()
    w = ''.join(c for c in w if c.isalnum())
    if not len(w):
        return word
    if w not in WORD_TO_EMOJI and w[-2:] == 'es':
        w = w[:-2] # peaches -> peach
    if w not in WORD_TO_EMOJI and w[-1] == 's':
        w = w[:-1] # aubergines -> aubergine
    if w not in WORD_TO_EMOJI and w[-3:] == 'ing':
        w = w[:-3] # hating -> hat
    if w in WORD_TO_EMOJI:
        e = random.choice(WORD_TO_EMOJI[w]) * \
            random.choice([1, 1, 1, 2, 2, 2, 3, 4, 5])
        if random.random() < 0.3:
            return e
        elif random.random() < 0.3:
            return e + ' ' + word
        return word + ' ' + e
    else:
        return word


def emojify(message):
    out = ''
    curr = ''
    splits = set(' ,.!?\n')
    for c in message:
        if c in splits:
            out += emojify_or_not_i_am_a_function_not_a_cop(curr)
            out += c
            curr = ''
        else:
            curr += c
    return out + emojify_or_not_i_am_a_function_not_a_cop(curr)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    poo = emojify(message.text)
    bot.sendMessage(poo, thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
    print(emojify('A face shown with a single finger and thumb resting on the chin, glancing upward. Used to indicate thinking, or deep thought.'))
    print(emojify('Thinking Face was approved as part of Unicode 8.0 in 2015 and added to Emoji 1.0 in 2015.'))
    print(emojify('is it a bird? is it a plane?'))
    print(emojify('aubergines everywhere'))
    print(emojify('train training train'))
    print(emojify('flying'))
    print(emojify('hating'))
    print(emojify('teaches of peaches'))
