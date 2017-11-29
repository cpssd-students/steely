'''Get the latest Bitcoin price (in USD and EUR)'''
import requests

__author__ = ('CianLR', 'byxor')
COMMAND = 'btc'

API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
RESP_TEMPLATE = """Bitcoin Price:
€{}
${}
Difference since last time: {}"""

last_euros = 100

class BitcoinException(Exception): pass
class BadHttpResponse(BitcoinException): pass
class MissingFields(BitcoinException): pass


def get_bitcoin_rates():
    response = requests.get(API_URL)    

    if not response.ok:
        message = "Error getting price. Response (code {}) {}".format(
            response.status_code, response.text)
        raise BadHttpResponse(message)
    
    j = response.json()
    
    if not _is_valid_response(j):
        message = "Response is missing fields: {}".format(str(j))
        raise MissingFields(message)
    
    euros = float(j['bpi']['EUR']['rate'])
    dollars = float(j['bpi']['USD']['rate'])
    return (euros, dollars)

    
def _is_valid_response(resp):
    return ('bpi' in resp and
            'EUR' in resp['bpi'] and 'rate' in resp['bpi']['EUR'] and
            'USD' in resp['bpi'] and 'rate' in resp['bpi']['USD'])


def percentage_increase(before, after):
    delta = after - before
    return (delta * 100) / before


def percentage_string(n):
    return "{0:+d}%".format(n)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    try:
        global last_euros
        euros, dollars = get_bitcoin_rates()
        increase = percentage_increase(last_euros, euros)
        message = RESP_TEMPLATE.format(euros, dollars, percentage_string(increase))
        last_euros = euros
    except BitcoinException as e:
        message = str(e)
    bot.sendMessage(message, thread_id=thread_id, thread_type=thread_type)
