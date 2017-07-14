import random


COMMAND = '.box'


def gen_box(word):
    yield '```'
    yield ' '*6 + ' '.join(word)
    yield ' '*4 + '/' + ' ' + word[1] + ' '*(2*len(word)-5) + '/' + ' ' + word[-2]
    yield ' '*2 + '/' + ' '*3 + word[2] + ' '*(2*len(word)-7) + '/' + ' '*3 + word[-3]
    yield ' '.join(word) + ' '*5 + word[-4]
    for n in range(len(word) - 5):
        yield word[n + 1] + ' '*5 + word[n+4] + ' '*(2*len(word) - 9) + word[-n-2] + ' '*5 + word[-n+len(word)-5]
    yield word[-4] + ' '*5 + ' '.join(word[::-1])
    yield word[-3] + ' '*3 + '/' + ' '*(2*len(word)-7) + word[2] + ' '*3 + '/'
    yield word[-2] + ' ' + '/' + ' '*(2*len(word)-5) + word[1] + ' /'
    yield ' '.join(word[::-1])
    yield '```'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage('word please', thread_id=thread_id, thread_type=thread_type)
    elif 5 < len(message) < 20:
        box = '\n'.join(gen_box(message))
        bot.sendMessage(box, thread_id=thread_id, thread_type=thread_type)
    else:
        bot.sendMessage("can't use \"{}\"".format(message), thread_id=thread_id, thread_type=thread_type)
