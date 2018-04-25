#!/usr/bin/python
# -*- coding: utf-8 -*-
'''find the location of a host. it can be a domain or an ip.'''
import requests

__author__ = 'devoxel'
COMMAND = 'pang'


def get(host):
    '''
    get(query) returns a string to represent the location of a host
    the api is described in http://freegeoip.net
    '''
    API = 'http://freegeoip.net/json/'

    req = requests.get(API + host)
    if req.status_code != 200:
        print('geoip.py: bad request for', host, 'status:', req.status_code)
        return None

    return build_output(req.json())


def build_output(info):
    # the builder is a list of (keys, display information
    # it's because i'm super lazy
    builder = [
        ('country_name', 'Country: '),
        ('region_name', 'Region: '),
        ('city', 'City: '),
        ('zip_code', 'Zip: '),
        ('time_zone', 'Time zone: '),
    ]

    def valid_info(k): return k in info and info[k]

    out = []
    for (k, o) in builder:
        if valid_info(k):
            out.append(o + str(info[k]))
    # since lat and long are on the same line they're a special case
    if valid_info('latitude') and valid_info('longitude'):
        out.append(f'{info["latitude"]}°N, {info["longitude"]}°E')

    return '\n'.join(out)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    if not message:
        # this would return steely's ip
        return
    o = get(message)
    if not o:
        return
    bot.sendMessage(o, thread_id=thread_id, thread_type=thread_type)


if __name__ == '__main__':
    print(get('github.com'))
    print(get('8.8.4.4'))
    print(get('frick off'))
