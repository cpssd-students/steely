from urllib.request import Request, urlopen
import json


def expand(url):
    API_ADDRESS = 'http://x.datasig.io/short?url={}'
    request_url = API_ADDRESS.format(url)
    request = Request(request_url)
    response_stream = urlopen(request)
    response = json.loads(response_stream.read().decode("utf-8"))
    response_stream.close()
    expanded_url = response['/short']['destination']
    return expanded_url


# --- Bot-related knowledge ----------------


COMMAND = '.exp'

NO_URL_MESSAGE = "Input Error: You didn't provide a URL..."


def main(bot, author_id, message, thread_id, thread_type, **kwargs):

    def send(text):
        bot.sendMessage(text, thread_id=thread_id, thread_type=thread_type)

    if message:
        short_url = message
        send(expand(short_url))
    else:
        send(NO_URL_MESSAGE)

