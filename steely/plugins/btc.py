'''Get the latest Bitcoin price (in USD and EUR)'''
import requests

__author__ = ('CianLR', 'byxor')
COMMAND = 'btc'

API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
RESP_TEMPLATE = """€{}
${}
difference since last time: {}"""
LAST_EUROS = 100

class BitcoinException(Exception):
    pass
class BadHTTPResponse(BitcoinException):
    pass
class MissingFields(BitcoinException):
    pass


def get_bitcoin_rates():
    response = requests.get(API_URL)
    if not response.ok:
        message = "Error getting price. Response (code {}) {}".format(
            response.status_code, response.text)
        raise BadHTTPResponse(message)
    response_json = response.json()
    if not _is_valid_response(response_json):
        message = "Response is missing fields: {}".format(str(response_json))
        raise MissingFields(message)
    euros = response_json['bpi']['EUR']['rate_float']
    dollars = response_json['bpi']['USD']['rate_float']
    return euros, dollars


def _is_valid_response(resp):
    return ('bpi' in resp and
            'EUR' in resp['bpi'] and 'rate' in resp['bpi']['EUR'] and
            'USD' in resp['bpi'] and 'rate' in resp['bpi']['USD'])


def percentage_increase(before, after):
    delta = after - before
    return (delta * 100) / before


def percentage_string(n):
    return "{:.3f}%".format(n)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    try:
        global LAST_EUROS
        euros, dollars = get_bitcoin_rates()
        increase = percentage_increase(LAST_EUROS, euros)
        message = RESP_TEMPLATE.format(euros, dollars, percentage_string(increase))
        LAST_EUROS = euros
    except BitcoinException as e:
        message = str(e)
    bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
