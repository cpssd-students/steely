'''
http://i0.kym-cdn.com/photos/images/original/001/042/049/5ef.jpg
'''
import requests
from paths import CONFIG

__author__ = 'CianLR'
COMMAND = '..'
API_URL = "https://api.deepai.org/api/deepdream"


def get_dream(url):
    resp = requests.post(
        API_URL,
        data={'content': url},
        headers={'api-key': CONFIG.DEEP_API_KEY},
    )
    return resp.status_code, None if resp.status_code != 200 else resp.json()


def grab_image(message):
    for a in message.attachments:
        # TODO: Something less stupid than below
        if a.__class__.__name__ == 'ImageAttachment':
            return a
    return None


def dream(bot, message, image_send, text_send):
    image = grab_image(message)
    if image is None:
        return text_send("Last message doesn't contain an image")
    text_send("Dreaming, please wait... (may take a few mins)")
    image_url = bot.fetchImageUrl(image.uid)
    code, dream = get_dream(image_url)
    if code != 200:
        return text_send("Non 200 HTTP code recieved: HTTP {}".format(code))
    if 'output_url' not in dream:
        return text_send("Some API error occured: {}".format(str(dream)))
    return image_send(dream['output_url'])


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    image_send = lambda url: bot.sendRemoteImage(url,
                                                 thread_id=thread_id,
                                                 thread_type=thread_type)
    text_send = lambda text: bot.sendMessage(text,
                                             thread_id=thread_id,
                                             thread_type=thread_type)
    dream(bot, message, image_send, text_send)


if __name__ == '__main__':
    harold = ('https://static.independent.co.uk/'
              's3fs-public/thumbnails/image/2017/07/11/11/harold-0.jpg')
    print(get_dream(harold))
