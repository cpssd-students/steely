from collections import namedtuple
import random


__author__ = 'byxor'
COMMAND = None
RESPONSE_CHANCE = 0.2


def main(bot, author_id, message, thread_id, thread_type, **kwargs):

    UNIVERSAL_RESPONSES = {
        "why does it matter?",
        "who cares?",
        "do you need to know?",
        "shut up",
        "ok sam",
    }

    PERSONAL_RESPONSES = {
        "i have a name, you know",
        "beep beep boop",
        "boop beep bop",
        "speaking",
        "does... not... compute...",
        "you know i'm a real person, right?",
        "i'm right here",
        "stop talking about me",
    }

    RESPONDERS = {
        
        new_responder("who", {
            "who do you think?",
            "who is sam?",
            "whoever you want, sunshine",
        }.union(UNIVERSAL_RESPONSES)),
        
        new_responder("what", {
            "what do you think?",
            "what do you mean by 'what'?",
        }.union(UNIVERSAL_RESPONSES)),

        new_responder("why", {
            "why do you need to know?",
            "why this? why that? stop asking questions",
            "why are traps considered to be gay?",
        }.union(UNIVERSAL_RESPONSES)),

        new_responder("how", {
            "how long is a piece of string?",
            "How Can Our Eyes Be Real If Mirrors Aren't Real?",
        }.union(UNIVERSAL_RESPONSES)),

        new_responder("bot", PERSONAL_RESPONSES),
        new_responder("reed", PERSONAL_RESPONSES),
        new_responder("steely", PERSONAL_RESPONSES),
    }
    
    response = search_for_response(RESPONDERS, message)
    if response:
        bot.sendMessage(response, thread_id=thread_id, thread_type=thread_type)


def new_responder(trigger_word, responses):
    def respond_to(message):
        chance_is_met = random.random() < RESPONSE_CHANCE
        if chance_is_met and should_respond(trigger_word, message):
            return get_response(responses)
    return respond_to


def should_respond(trigger_word, message):
    return trigger_word.lower() in message.lower()


def get_response(responses):
    return random.choice(list(responses))


def search_for_response(responders, message):
    for responder in responders:
        response = responder(message)
        if response:
            return response
    return None
        
