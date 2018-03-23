'''pester senan by reminding him how many PR's are waiting'''


import requests


__author__ = 'alexkraak'
COMMAND = 'steelygh'


PROTOCOL = 'https'
DOMAIN = 'github.com'
REPOSITORY = 'sentriz/steely'

API_URL = f'{PROTOCOL}://api.{DOMAIN}/repos/{REPOSITORY}'
REGULAR_URL = f'{PROTOCOL}://{DOMAIN}/{REPOSITORY}'


def handle_prs():
    pulls = requests.get(f'{API_URL}/pulls').json()
    message = f'Senan, you have {len(pulls)} fucken pr\'s to merge.' + \
              f'\n{REGULAR_URL}/pulls'
    return message


def handle_last():
    url = f'{API_URL}/commits'
    commits = requests.get(url).json()
    return 'Last commit was "{}" by {}'.format(commits[0]['commit']['message'],
                                             commits[0]['commit']['author']['name'])

SUBCOMMANDS = {
    'prs': handle_prs,
    'last': handle_last,
}


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = message or 'prs'
    output = "Valid commands: " + ', '.join(SUBCOMMANDS)
    if message in SUBCOMMANDS:
        output = SUBCOMMANDS[message]()
    bot.sendMessage(output, thread_id=thread_id, thread_type=thread_type)
