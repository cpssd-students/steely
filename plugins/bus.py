#!/usr/bin/env python3

import json
import requests


COMMAND = '.dbus'
BASE_URL = "http://data.dublinked.ie/cgi-bin/rtpi/"


def next_bus_realtime(stop_id):
    url = BASE_URL + "realtimebusinformation?stopid={}&format=json".format(stop_id)
    response = requests.get(url).json()
    done_routes = []
    for arrival in response['results']:
        if arrival["route"] in done_routes:
            continue
        yield arrival["route"], arrival["duetime"], arrival["destination"]
        done_routes.append(arrival["route"])


def gen_reply_string(arrivals):
    max_route = max(len(arrival[0]) for arrival in arrivals)
    max_duetime = max(len(arrival[1]) for arrival in arrivals)
    max_dest = max(len(arrival[2]) for arrival in arrivals)
    yield "```"
    for route, duetime, destination in arrivals:
        yield '{route:<{max_route}} {destination:<{max_dest}} {duetime:>{max_duetime}}min'.format_map(locals())
    yield "```"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage("please include a stop number", thread_id=thread_id, thread_type=thread_type)
        return
    try:
        arrivals = list(next_bus_realtime(message))
    except requests.exceptions.RequestException:
        bot.sendMessage("error retrieving results", thread_id=thread_id, thread_type=thread_type)
        return
    if not arrivals:
        bot.sendMessage("no buses found >:(", thread_id=thread_id, thread_type=thread_type)
        return
    bot.sendMessage("\n".join(gen_reply_string(arrivals)), thread_id=thread_id, thread_type=thread_type)


if __name__ == "__main__":
    arrivals = list(next_bus_realtime("37"))
    print("\n".join(gen_reply_string(arrivals)))
