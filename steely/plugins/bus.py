#!/usr/bin/env python3
'''
.dbus <stop id>

list dublin bus times for a given stop id
'''


import json
import requests
from collections import namedtuple
import operator


COMMAND = '.dbus'
BASE_URL = "http://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation"
COLUMNS =  ('route', 'destination', 'duetime')


def next_bus_realtime(stop_id):
    params = {
        'stopid': stop_id,
        'format': 'json',
    }
    response = requests.get(BASE_URL, params=params).json()
    for arrival in response['results']:
        yield arrival


def arrival_sort(arrival):
    if arrival['duetime'] == 'Due':
        return 0
    sort_column = COLUMNS[-1]
    return int(arrival[sort_column])


def gen_reply_string(arrivals):
    arrivals = list(arrivals)
    def max_string(column):
        return max(len(str(arrival[column])) for arrival in arrivals)
    max_route, max_dest, max_duetime = map(max_string, COLUMNS)
    yield "```"
    for arrival in sorted(arrivals, key=arrival_sort):
        due_suffix, extra_due_padding = 'min', 0
        if not arrival['duetime'].isdigit():
            due_suffix = ''
            extra_due_padding = 3
            arrival['duetime'] = 'due'
        yield f'{arrival["route"]:<{max_route}} ' + \
              f'{arrival["destination"]:<{max_dest}} ' + \
              f'{arrival["duetime"]:>{max_duetime + extra_due_padding}}{due_suffix}'
    yield "```"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not message:
        send_message("please include a stop number")
        return
    arrivals = next_bus_realtime(message)
    if not arrivals:
        send_message("no buses found >:(")
        return
    send_message("\n".join(gen_reply_string(arrivals)))


if __name__ == "__main__":
    # print("\n".join(gen_reply_string(next_bus_realtime(37))))
    print("\n".join(gen_reply_string(next_bus_realtime(1995))))
    # print("\n".join(gen_reply_string(next_bus_realtime(91))))
