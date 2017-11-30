from nose.tools import *
from steely.plugins.responder import *


def test_response_check():
    data = [
        ("why", "why do you think?", True),
        ("why", "Why do you think?", True),
        ("why", "What do you think?", False),
        ("what", "What do you think?", True),
        ("what", "what do you think?", True),
        ("WHAT", "what do you think?", True),
        ("who", "I don't know, who are you?", True),
    ]
    for trigger_word, message, expected in data:
        yield assert_equal, expected, should_respond(trigger_word, message)


def test_responses():
    data = [
        ["x"],
        ["a", "b", "c"],
        ["foo", "bar", "baz"],
    ]
    for responses in data:
        result = get_response(set(responses))
        yield assert_in, result, responses
