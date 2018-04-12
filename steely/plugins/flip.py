'''My life got flipped, turned upside down'''


__author__ = 'iandioch'
COMMAND = 'flip'

NORMAL = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
FLIPPED = 'ɐqɔpǝⅎƃɥᴉɾʞʅɯuodbɹsʇnʌʍxʎz∀ꓭϽᗡƎᖵ⅁HIᒋꓘ⅂ꟽNOԀꝹꓤSꓕՈɅϺX⅄Z'

FROM = NORMAL + FLIPPED
TO = FLIPPED + NORMAL
FLIP_TRANS = str.maketrans(FROM, TO)


def flip(string):
    return '\u200F' + string.translate(FLIP_TRANS)[::-1]


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(flip(message.text), thread_id=thread_id,
                    thread_type=thread_type)
