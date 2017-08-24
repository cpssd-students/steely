'''pester senan by reminding him how many PR's are waiting'''


import requests


__author__ = 'alexkraak'
COMMAND = '.steelygh'


def handle_prs():
    pulls = requests.get('https://api.github.com/repos/sentriz/steely/pulls').json()
    return 'Senan, you have {} fucken pr\'s to merge'.format(len(pulls))


def handle_last():
    url = 'https://api.github.com/repos/sentriz/steely/commits'
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
