import requests


COMMAND = '.xkcd'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    response = requests.get("https://xkcd.com/info.0.json")
    image = response.json()['img']
    message = response.json()['alt']   
    bot.sendRemoteImage(image, message=message, thread_id=thread_id, thread_type=thread_type)
