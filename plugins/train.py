import requests
import re


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
    duein = re.findall(duein_pattern, xml)
    duein = [int(i) for i in duein]

    # merge duein & destination to 2d list
    reply = sorted([list(a) for a in zip(duein, destination)])

    return '\n'.join(str(due) + ' minutes until train to ' + dest for due, dest in reply[0:3])

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        bot.sendMessage("Invalid train station", thread_id=thread_id, thread_type=thread_type)
        return
    try:
        reply_string = '\n'.join(get_train_times(message))
        bot.sendMessage(reply_string, thread_id=thread_id, thread_type=thread_type)
    except requests.exceptions.RequestException:
        bot.sendMessage("error retrieving results", thread_id=thread_id, thread_type=thread_type)
