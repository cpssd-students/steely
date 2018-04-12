'''.sentiment tracks user positivity or negativity in previous message for all the autismos'''
import requests
import json


__author__ = 'oskarmcd'
COMMAND = 'sentiment'
BASE_URL = 'http://text-processing.com/api/sentiment/'
FULL_STRINGS = {
    'pos': 'positive',
    'neg': 'negative',
    'neutral': 'neutral'
}


def sanitized(input):
    replacements = (('`', ''),
                    ('\n', ' '))
    for bad, good in replacements:
        input = input.replace(bad, good)
    return input


def get_sentiment(string):
    response = requests.post(BASE_URL, f'text={string}')
    data = response.json()
    probability = data['probability']
    body = f"The phrase you've checked is {string!r}.\n"
    for feeling in FULL_STRINGS:
        body += f"We're {probability[feeling] * 100:.2f}% sure " + \
            f"the message is {FULL_STRINGS[feeling]}\n"
    conclusion = FULL_STRINGS[data['label']]
    body += f"I'm gonna guess this shit is {conclusion}"
    return body


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    last_message = bot.fetchThreadMessages(
        thread_id=thread_id, limit=2)[1].text
    if len(last_message) > 150:
        send_message('no')
        return
    last_message = sanitized(last_message)
    send_message(get_sentiment(last_message))
