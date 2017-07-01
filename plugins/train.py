import urllib.request
import urllib.error
import re


COMMAND = '.train'
BASE_URL = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc='



def get_train_times(station):
    url = BASE_URL + station.replace(' ', '+')
    xml = str(urllib.request.urlopen(url).read())

    # regex patterns
    destination_pattern = '(?:<Destination>)(\w+)(?:<\/Destination>)'
    duein_pattern = '(?:<Duein>)(\d+)(?:<\/Duein>)'
    # capture strings
    destination = re.findall(destination_pattern, xml)
    duein = re.findall(duein_pattern, xml)

    if 0 < len(destination):
        yield duein[0] + " minutes until train to " + destination[0]


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage("Invalid train station", thread_id=thread_id, thread_type=thread_type)
        return
    try:
        reply_string = '\n'.join(get_train_times(message))
        bot.sendMessage(reply_string, thread_id=thread_id, thread_type=thread_type)
    except urllib.error.HTTPError:
        bot.sendMessage("error retrieving results", thread_id=thread_id, thread_type=thread_type)
