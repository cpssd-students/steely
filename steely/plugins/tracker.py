'''
.tracker <tracker>
.tracker list
'''


import requests
from operator import itemgetter


COMMAND = '.tracker'
BASE = 'https://{tracker}.trackerstatus.info/api/all/'
TRACKERS = ('ar', 'nwcd', 'btn', 'ptp', 'mtv', 'red', 'ggn')


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if message == 'list':
        bot.sendMessage(", ".join(TRACKERS),
                        thread_id=thread_id, thread_type=thread_type)
        return
    if not message:
        bot.sendMessage("please provide one of " + ", ".join(TRACKERS),
                        thread_id=thread_id, thread_type=thread_type)
        return
    response = requests.get(BASE.format(tracker=message)).json()
    max_service = max(len(key) for key in response)
    max_latency = max(len(info["Latency"]) for info in response.values())
    string = "```\n"
    for service, info in sorted(response.items(), key=itemgetter(0)):
        print(service, info)
        string += "{service:<{max_service}} {latency:>{max_latency}}\n".format(
            latency=info["Latency"], **locals())
    bot.sendMessage(string + "```",
                    thread_id=thread_id, thread_type=thread_type)
