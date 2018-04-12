#!/usr/bin/env python3
'''
.dbus <stop id>

list dublin bus times for a given stop id
'''


from collections import namedtuple
import json
import operator
import re
import requests
from formatting import *


__author__ = 'alexkraak'
COMMAND = 'dbus'
BASE_URL = "http://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation"
COLUMNS =  ('route', 'destination', 'duetime')


def next_bus_realtime(stop_id):
    params = {
        'stopid': stop_id,
        'format': 'json',
    }
    response = requests.get(BASE_URL, params=params).json()
    for arrival in response['results']:
        yield sanitized(arrival)


def arrival_sort(arrival):
    if arrival['duetime'] == 'due':
        return 0
    sort_column = COLUMNS[-1]
    return arrival[sort_column]


def sanitized(arrival):
    dirty_duetime = arrival['duetime']
    dirty_dest = arrival['destination']
    street_match = r'\b(Street|St)(?![\w\.])'
    if dirty_duetime == 'Due':
        arrival['duetime'] = 'due'
    elif dirty_duetime.isdigit():
        arrival['duetime'] = int(dirty_duetime)
    arrival['destination'] = re.sub(street_match, 'St.', dirty_dest)
    return arrival


def gen_reply_string(arrivals):
    arrivals = list(arrivals)
    def max_string(column):
        return max(len(str(arrival[column])) for arrival in arrivals)
    max_route, max_dest, max_duetime = map(max_string, COLUMNS)
    if len(arrivals) <= 0:
        yield ""
    else:
        for arrival in sorted(arrivals, key=arrival_sort):
            due_suffix, extra_due_padding = 'min', 0
            if arrival['duetime'] == 'due':
                due_suffix = ''
                extra_due_padding = 3
            yield f'{arrival["route"]:<{max_route}} ' + \
                f'{arrival["destination"]:<{max_dest}} ' + \
                f'{arrival["duetime"]:>{max_duetime + extra_due_padding}}{due_suffix}'


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
    send_message(code_block("\n".join(gen_reply_string(arrivals))))


if __name__ == "__main__":
    # print("\n".join(gen_reply_string(next_bus_realtime(37))))
    print("\n".join(gen_reply_string(next_bus_realtime(1995))))
    # print("\n".join(gen_reply_string(next_bus_realtime(91))))
