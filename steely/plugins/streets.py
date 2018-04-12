#!/usr/bin/env python3
"""This plugin tells you if your idea is good or not."""

import random

__author__ = 'CianLR'
COMMAND = None

RESP_CHANCE = 0.5
RESP_TRIGGERS = {"i think"}


def get_response(message):
    if (not any(trigger in message.lower() for trigger in RESP_TRIGGERS) or
            random.random() > RESP_CHANCE):
        return None
    return random.choice(["That's streets ahead dude",
                          "Man you're streets behind"])


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    resp = get_response(message)
    if resp:
        bot.sendMessage(resp, thread_id=thread_id, thread_type=thread_type)


if __name__ == '__main__':
    for _ in range(10):
        print(get_response("I think the world is flat"))
