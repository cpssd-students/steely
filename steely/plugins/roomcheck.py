#!/usr/bin/env python3
'''
.room <room number>

Check if a dcu room is free right now

.room <GLA.LG26>
'''


import requests
from datetime import datetime
import sys
import bs4


__author__ = 'gruunday'
COMMAND = '.room'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not message:
        send_message('.room <room number>\nCheck if a dcu room is free right now\n.room <GLA.LG26>')
        return
    booking = check_room(message)
    if booking:
        send_message(message + ' is not free, there is\n \n' + booking + '\n')
    else:
        send_message(message + " is currently free\n")


def check_room(room):
    url = get_url(room)
    # Downloads request from url URL and stores as string in res
    res = requests.get(url)
    # Creates Beautiful Soup out of html
    current_soup = bs4.BeautifulSoup(res.text, "lxml")
    # Takes all <tr> tags
    elems = current_soup.select('tr')
    return elems[14].getText().strip()


def get_url(room):
    baseurl = 'https://www101.dcu.ie/timetables/feed.php?'
    week = get_week()
    hour = get_hour()
    day = get_day()
    template = 'location'
    return ('%sroom=%s&week1=%s&hour=%s&day=%s&template=%s'
            % (baseurl, room, week, hour, day, template))


def get_week():
    # Stub must replace
    week_number = 1
    return week_number


def get_day():
    return datetime.date(datetime.now()).isoweekday()


def get_hour():
    date = datetime.now()
    hour = str(date).split()[1][0:2]
    minute = str(date).split()[1][3:5]
    if int(minute) > 30:
        inthour = int(hour)
        inthour += 1
    return str(inthour - 8)


if __name__ == '__main__':
    main()
