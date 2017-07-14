#!/usr/bin/env python3

import requests
import re
from operator import itemgetter


COMMAND = '.train'
BASE_URL = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc='


def get_train_times(station):
    url = BASE_URL + station.replace(' ', '+')
    xml = requests.get(url)
    xml = str(xml.text)

    # regex patterns
    destination_pattern = '(?:<Destination>)(\w+)(?:<\/Destination>)'
    duein_pattern = '(?:<Duein>)(\d+)(?:<\/Duein>)'
    destination = re.findall(destination_pattern, xml)
    duein = map(int, re.findall(duein_pattern, xml))

    # merge duein & destination to 2d list
    yield from sorted(zip(destination, duein), key=itemgetter(1))[:3]


def gen_reply_string(times):
    yield "```"
    max_destin = max(len(line[0]) for line in times)
    max_time = max(len(str(line[1])) for line in times)
    for destin, time in times:
        yield "{destin:<{max_destin}} {time:>{max_time}}min".format_map(locals())
    yield "```"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage("Invalid train station", thread_id=thread_id, thread_type=thread_type)
        return
    try:
        times = list(get_train_times(message))
    except requests.exceptions.RequestException:
        bot.sendMessage("error retrieving results", thread_id=thread_id, thread_type=thread_type)
    if times:
        bot.sendMessage("\n".join(gen_reply_string(times)), thread_id=thread_id, thread_type=thread_type)
    else:
        bot.sendMessage("no results", thread_id=thread_id, thread_type=thread_type)



if __name__ == "__main__":
    times = list(get_train_times("bayside"))
    print("\n".join(gen_reply_string(times)))

