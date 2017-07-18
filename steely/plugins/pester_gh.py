'''pester senan by reminding him how many PR's are waiting'''


import requests


COMMAND = '.steelygh'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    pulls = requests.get('https://api.github.com/repos/sentriz/steely/pulls').json()
    bot.sendMessage('Senan, you have {} fucken pr\'s to merge\nhttps://github.com/sentriz/steely/pulls'.format(len(pulls)),
                    thread_id=thread_id, thread_type=thread_type)
