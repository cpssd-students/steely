# sendRemoteImage(image_url, message=None, thread_id=None, thread_type=ThreadType.USER)
import requests

COMMAND = '.xkcd'

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    r = requests.get("https://xkcd.com/info.0.json")
    img = r.json()['img']
    msg = r.json()['alt']   
    bot.sendRemoteImage(img, message=msg, thread_id=thread_id, thread_type=thread_type)
