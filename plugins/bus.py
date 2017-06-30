import json
import requests


COMMAND = '.dbus'
BASE_URL = "http://data.dublinked.ie/cgi-bin/rtpi/"


def get_stop_routes(stop_id):
    url = BASE_URL + "busstopinformation?stopid={}&format=json".format(stop_id)
    response = requests.get(url).json()
    for result in response["results"]:
        for operator in result['operators']:
            yield from operator['routes']


def next_bus_realtime(stop_id, routes):
    url = BASE_URL + "realtimebusinformation?stopid={}&format=json".format(stop_id)
    base_str_format = "{} should arrive in {} mins, heading to {}\n\n"
    response = requests.get(url).json()
    done = []
    for arrival in response['results']:
        if arrival['route'] in done:
            continue
        done.append(arrival['route'])
        yield base_str_format.format(arrival['route'],
                                     arrival['duetime'],
                                     arrival['destination'])


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage("please include a stop number", thread_id=thread_id, thread_type=thread_type)
        return
    try:
        reply_string = '\n'.join(next_bus_realtime(message, get_stop_routes(message)))
        bot.sendMessage(reply_string, thread_id=thread_id, thread_type=thread_type)
    except requests.exceptions.RequestException:
        bot.sendMessage("error retrieving results", thread_id=thread_id, thread_type=thread_type)
