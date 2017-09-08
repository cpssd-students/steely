#!/usr/bin/env python3
'''
.train <train station>

get irish rail train state times
'''


import requests
import re
from operator import itemgetter
from xml.etree import ElementTree


__author__ = 'izaakf'
COMMAND = '.train'
NAMESPACES = {'realtime': 'http://api.irishrail.ie/realtime/'}
REALTIME_URL = f"{NAMESPACES['realtime']}realtime.asmx/getStationDataByNameXML"


def get_train_times(station):
    params = {'StationDesc': station}
    response = requests.get(REALTIME_URL, params=params).text
    response_tree = ElementTree.fromstring(response)
    for station in response_tree.findall('realtime:objStationData', NAMESPACES):
        yield parse_direction(station.find('./realtime:Direction', NAMESPACES).text), \
                              station.find('./realtime:Origin', NAMESPACES).text, \
                              station.find('./realtime:Destination', NAMESPACES).text, \
                              station.find('./realtime:Duein', NAMESPACES).text


def parse_direction(direction):
    aliases = {'Northbound': '↑',
               'Southbound': '↓'}
    return aliases.get(direction, '-')


def len_longest_string_of(column):
    return max(len(str(row)) for row in column)


def gen_column_widths(times):
    for column in zip(*times):
        print(column)
        yield len_longest_string_of(column)


def gen_reply_string(times, widths):
    _, max_origin, max_destin, max_time = widths
    yield "```"
    yield f"  {'from':<{max_origin}} to"
    for direction, origin, destin, time in times:
        yield f"{direction} {origin:<{max_origin}} {destin:<{max_destin}} {time:>{max_time}}min"
    yield "```"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not message:
        send_message("invalid train station", thread_id=thread_id, thread_type=thread_type)
        return
    try:
        times = list(get_train_times(message))
        widths = gen_column_widths(times)
    except requests.exceptions.RequestException:
        send_message("error retrieving results")
    if times:
        send_message("\n".join(gen_reply_string(times, widths)))
    else:
        send_message("no results")


if __name__ == "__main__":
    times = list(get_train_times("bayside"))
    widths = gen_column_widths(times)
    print("\n".join(gen_reply_string(times, widths)))
