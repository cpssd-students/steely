'''🆒'''

import random
import requests
from collections import defaultdict

__author__ = ('iandioch')
COMMAND = 'emoji'

EMOJI_DATA = {}
try:
    EMOJI_DATA = requests.get('https://raw.githubusercontent.com/muan/emojilib/master/emojis.json').json()
except Exception as e:
    print('No emoji data for you sir! Good day!')
    print(e)

BLACKLIST = set([
    'to',
    'in',
    'at'
])
WORD_TO_EMOJI = defaultdict(list)

for k in EMOJI_DATA:
    if 'keywords' not in EMOJI_DATA[k]:
        continue
    emoji = EMOJI_DATA[k]['char']
    if emoji is None:
        continue
    WORD_TO_EMOJI[k].append(emoji)
    for word in EMOJI_DATA[k]['keywords']:
        if word in BLACKLIST:
            continue
        WORD_TO_EMOJI[word].append(emoji)

def emojify_or_not_i_am_a_function_not_a_cop(word):
    word = word.lower()
    if word in WORD_TO_EMOJI:
        e = random.choice(WORD_TO_EMOJI[word])*random.choice([1, 1, 1, 2, 2, 3])
        if random.random() < 0.3:
            return e
        return word + e
    else:
        return word

def emojify(message):
    out = ''
    curr = ''
    splits = set(' .!?')
    for c in message:
        if c in splits:
            out += emojify_or_not_i_am_a_function_not_a_cop(curr)
            out += c
            curr = ''
        else:
            curr += c
    return out + curr

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    poo = emojify(message.text)
    bot.sendMessage(poo, thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
    print(emojify('A face shown with a single finger and thumb resting on the chin, glancing upward. Used to indicate thinking, or deep thought.'))
    print(emojify('Thinking Face was approved as part of Unicode 8.0 in 2015 and added to Emoji 1.0 in 2015.'))
