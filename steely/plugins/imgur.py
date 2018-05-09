'''
Get the latest image from Imgur, potentially NSFW.
'''
import requests
from html import unescape

__author__ = 'CianLR'
COMMAND = 'imgur'
LATEST_URL = "https://imgur.com/new/time"


def extract(s, start, end, init_pos=0):
    start_pos = s.find(start, init_pos) + len(start)
    if start_pos == -1:
        return None
    end_pos = s.find(end, start_pos)
    if end_pos == -1:
        return None
    return s[start_pos:end_pos]


def imgur_thumbnail_to_full(url):
    ext, rest = url[::-1].split('.', 1)
    assert rest[0] == 'b'  # This must be a b to be a thumbnail
    return (ext + '.' + rest[1:])[::-1]


def get_latest_imgur():
    r = requests.get(LATEST_URL)
    r.encoding = 'utf-8'
    if r.status_code != requests.codes.ok:
        return "Status code {}".format(r.status_code), None
    # Get URL
    url = extract(r.text, '<img alt="" src="', '" />')
    if url is None:
        return "Could not extract url", None
    # Get title
    title = extract(r.text, '<p>', '</p>', r.text.find(url))
    if title is None:
        return "Could not extract title", None
    return unescape(title), imgur_thumbnail_to_full('https:' + url)


def imgur(image_send, text_send):
    message, image_url = get_latest_imgur()
    if image_url is None:
        text_send("Unable to get image: {}".format(message))
        return
    text_send(message)
    image_send(image_url)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    image_send = lambda url: bot.sendRemoteImage(url,
                                                 thread_id=thread_id,
                                                 thread_type=thread_type)
    text_send = lambda text: bot.sendMessage(text,
                                             thread_id=thread_id,
                                             thread_type=thread_type)
    imgur(image_send, text_send)


if __name__ == '__main__':
    imgur(lambda s: print("URL sent: " + s),
          lambda s: print("Text sent: " + s))

