'''Got a great idea? Search for existing trademarks with `.tm <myidea>`'''
import random
import requests

from steely import config

__author__ = 'CianLR'
COMMAND = 'tm'
URL = "https://www.markerapi.com/api/v1/trademark/search/*{}*/username/{}/password/{}"
REQUIRED_KEYS = ["wordmark", "serialnumber", "registrationdate", "description"]
RESPONSE_TEMPLATE = """Name: {wordmark}
SN: {serialnumber}
Date: {registrationdate}
Description: {description}"""

def full_result(res):
    """Check the API returned a result with enough info"""
    return all(key in res for key in REQUIRED_KEYS)


def tm(term):
    if not config.TM_API_USER or not config.TM_API_PASS:
        return ".tm is unconfigured!"

    if len(term) < 3:
        return "Search term must be at least 3 chars (or the API gets _slow_)"

    filled_url = URL.format(term, config.TM_API_USER, config.TM_API_PASS)
    resp = requests.get(filled_url)
    if resp.status_code != 200:
        return "Error code {}!".format(resp.code)
    
    trademarks = resp.json()
    if trademarks['count'] == 0:
        return "No results!"

    valid_tms = [tm for tm in trademarks['trademarks'] if full_result(tm)]
    if len(valid_tms) == 0:
        return "No detailed trademarks"
    return RESPONSE_TEMPLATE.format(**random.choice(valid_tms))


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    bot.sendMessage(tm(message), thread_id=thread_id, thread_type=thread_type)


if __name__ == '__main__':
    tests = ['tayne', 'steely', 'lou', 'qwdfghtresxcghytrdcv']
    for t in tests:
        print(t + '\n' + tm(t) + '\n')

