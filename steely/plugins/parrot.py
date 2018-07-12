'''
Get ready to party boiz.

Just hit that .party after an image is posted and have it turned into a
beautiful party parrot. Non-square images will be resized with extreme
prejudice.
'''
import urllib

__author__ = 'CianLR'
COMMAND = 'party'
API_URL = "https://ppaas.herokuapp.com/partyparrot/mega?{}"
API_ARGS = {
    'overlay': None,
    'overlayWidth': 140,
    'overlayHeight': 140,
    'overlayOffsetX': -30,
    'overlayOffsetY': -60,
}


def get_this_party_started(image_url):
    API_ARGS['overlay'] = image_url  # Lol, global state
    return API_URL.format(urllib.parse.urlencode(API_ARGS))


def grab_image(message):
    for a in message.attachments:
        # TODO: Something less stupid than below
        if a.__class__.__name__ == 'ImageAttachment':
            return a
    return None


def party(bot, message, image_send, text_send):
    image = grab_image(message)
    if image is None:
        return text_send("Last message doesn't contain an image")
    image_url = bot.fetchImageUrl(image.uid)
    party_url = get_this_party_started(image_url)
    image_send(party_url)
    return party_url


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    image_send = lambda url: bot.sendRemoteImage(url,
                                                 thread_id=thread_id,
                                                 thread_type=thread_type)
    text_send = lambda text: bot.sendMessage(text,
                                             thread_id=thread_id,
                                             thread_type=thread_type)
    party(bot, message, image_send, text_send)


if __name__ == '__main__':
    # This is how we test things in Google.
    harold = ('https://static.independent.co.uk/'
              's3fs-public/thumbnails/image/2017/07/11/11/harold-0.jpg')
    class ImageAttachment:
        uid = 'uid'
    class B:
        def fetchImageUrl(self, _):
            return harold
        attachments = [ImageAttachment()]
    party(B(), B(), print, print)

