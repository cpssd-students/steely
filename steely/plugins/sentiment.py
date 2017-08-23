'''.sentiment tracks user positivity or negativity in previous message for all the autismos'''
import requests
import json


COMMAND = '.sentiment'
BASE_URL = 'http://text-processing.com/api/sentiment/'
FULL_STRINGS = {
    'pos': 'positive',
    'neg': 'negative',
    'neutral': 'neutral'
}


def get_sentiment(string):
    response = requests.post(BASE_URL, f'text={string}')
    data = response.json()
    probability = data['probability']
    body =  f"The phrase you've checked is {string!r}.\n"
    body += f"We're {probability['pos'] * 100:.2f}% sure the message is positive\n"
    body += f"We're {probability['neg'] * 100:.2f}% sure the message is negative\n"
    body += f"We're {probability['neutral'] * 100:.2f}% sure the message is neutral\n"
    conclusion = FULL_STRINGS[data['label']]
    body += f"I'm gonna guess this shit is {conclusion}"
    return body


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    last_message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1].text
    if len(last_message) > 300:
        send_message('no')
        return
    send_message(get_sentiment(last_message))
