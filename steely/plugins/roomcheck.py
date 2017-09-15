#!/usr/bin/env python3
'''
.room <room number>

Check if a dcu room is free right now

.room GLA.LG26
'''


import requests
import datetime
import sys
import bs4


__author__ = 'gruunday'
COMMAND = '.room'
BASEURL = 'https://www101.dcu.ie/timetables/feed.php'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    def send_message(message):
        bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
    if not message:
        send_message(__doc__)
        return
    room_number = parse_room_number(message.upper())
    try:
        booking, link = get_booking(room_number)
    except ValueError:
        send_message('Building is closed at this time')
    if booking:
        send_message(f'{room_number} is not free, there is\n\n' + \
                     f'{booking}')
    else:
        send_message(f'{room_number} is currently free')
    send_message(link)


def parse_room_number(room_number):
    campus_codes = ('GLA.', 'SPD.')
    default_campus = campus_codes[0]
    if not any(campus in room_number for campus in campus_codes):
        room_number = default_campus + room_number
    return room_number


def get_booking(room, baseurl=None):
    baseurl = baseurl or BASEURL
    params = build_request_parameters(room)
    response = requests.get(baseurl, params=params)
    current_soup = bs4.BeautifulSoup(response.text, "lxml")
    elements = current_soup.select('tr')
    print(baseurl, params)
    return elements[14].getText().strip(), response.url


def build_request_parameters(room_number):
    now = datetime.datetime.now()
    return {'room': room_number,
            'week': academic_week_number(now),
            'hour': academic_hour(now),
            'day':  now.isoweekday(),
            'template': 'location'}


def academic_week_number(date):
    iso_year, iso_week_number, iso_weekday = date.isocalendar()
    academic_start_week = 36
    if iso_week_number >= academic_start_week:
        academic_offset = -academic_start_week
    else:
        academic_offset = 52 - academic_start_week
    academic_week = iso_week_number + academic_offset
    return academic_week


def academic_hour(date):
    hour = date.hour
    if hour < 8 or hour > 21:
        raise ValueError
    minute = date.minute
    if minute > 30:
        hour += 1
    return hour - 8


if __name__ == '__main__':
    print(get_booking('GLA.LG26'))
    print(get_booking('LG26'))
