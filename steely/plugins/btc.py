'''Get the latest Bitcoin price (in USD and EUR)'''
import requests

__author__ = 'CianLR'
COMMAND = 'btc'

API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
RESP_TEMPLATE = """Bitcoin Price:
    €{}
    ${}"""

def is_valid_response(resp):
    return ('bpi' in resp and
            'EUR' in resp['bpi'] and 'rate' in resp['bpi']['EUR'] and
            'USD' in resp['bpi'] and 'rate' in resp['bpi']['USD'])

def get_btc():
    response = requests.get(API_URL)
    if not response.ok:
        return "Error getting price. Response (code {}) {}".format(
            response.status_code, response.text)
    j = response.json()
    if not is_valid_response(j):
        return "Response is missing fields: {}".format(str(j))
    return RESP_TEMPLATE.format(j['bpi']['EUR']['rate'],
                                j['bpi']['USD']['rate'])

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(get_btc(), thread_id=thread_id, thread_type=thread_type)

if __name__ == '__main__':
    print(get_btc())

