'''gives the previous command m a y o n n a i s e'''

import random
import re
import string

__author__ = ('iandioch')
COMMAND = 'mayo'

FORMATS = [
    'Ara, {}!',
    '{} ara.',
    'ara {}.',
    '{} #mayo4sam',
    '{} #mayoforsam',
]


def mayo(message):
    message += ' '
    message = message.lower()
    message = message.replace('the', 'de')  # !important
    message = message.replace('s', 'sh')
    message = message.replace('sh ', 's ')
    message = message.replace('shh', 'sh')
    sentences = re.split('[.,!?]', message)
    out = ''
    for s in sentences:
        if random.random() < 0.4:
            out += random.choice(FORMATS).format(s) + ' '
        else:
            out += s + ' '
    return out


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    mayonnaise = mayo(message.text)
    bot.sendMessage(mayonnaise, thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
    print(mayo('lorem ipsum dolor sit amet'))
    print(mayo('Brexit: Barnier warns UK there is ‘no going back’ on deal'))
    print(mayo('Abortion committee set to recommend allowing terminations up to 12 weeks'))
    print(mayo('cash'))
