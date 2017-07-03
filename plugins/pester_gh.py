import requests


COMMAND = '.steelygh'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    pulls = requests.get('https://api.github.com/repos/sentriz/steely/pulls').json()
    bot.sendMessage('Senan, you have {} fucken pr\'s to merge'.format(len(pulls)),
                    thread_id=thread_id, thread_type=thread_type)
