from paths import CONFIG
import requests

__author__ = 'devoxel'
COMMAND = 'beer'

URL = 'http://api.brewerydb.com/v2/'
SEARCH = URL + "search/"
API_KEY = CONFIG.BREWERYDB_API_KEY

ERR_NO_RESULTS = "ah now we got no results"
ERR_API_LIMIT = "we used up all our api juice, try again tomorrow"
ERR_WHAT = "no idea whats going on"


def search_request(query):
    payload = {
        'q':    query,
        'type': 'beer',
        'key':  API_KEY,
    }
    response = requests.get(SEARCH, params=payload)
    if response.status_code != 200:
        raise ValueError(ERR_API_LIMIT)
    return response.json()


def format_output(response):
    if 'data' not in response:
        raise ValueError(ERR_NO_RESULTS)
    beer = response['data']
    if len(beer) == 0:
        raise ValueError(ERR_NO_RESULTS)
    # just take the first result
    beer = beer[0]
    output_format = [
        ('{}',        ['nameDisplay']),
        ('abv: {}%',  ['abv']),
        ('style: {}', ['style', 'shortName']),
    ]
    out = []
    for template, keys in output_format:
        o = beer
        for v in keys:
            if v not in o:
                o = None
                break
            o = o[v]
        if o:
            out.append(template.format(o))
    if not out:
        raise ValueError(ERR_WHAT)
    img_url = None
    if 'labels' in beer:
        img_url = beer['labels']['medium']
    return '\n'.join(out), img_url


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    try:
        response = search_request(message)
        desc, url = format_output(response)
    except ValueError as exc:
        bot.sendMessage(str(exc), thread_id=thread_id, thread_type=thread_type)
        return
    if url:
        bot.sendRemoteImage(url, thread_id=thread_id, thread_type=thread_type)
    bot.sendMessage(desc, thread_id=thread_id, thread_type=thread_type)


if __name__ == "__main__":
    import sys
    desc, url = searcher(sys.argv[1])
    print(desc)
    print("---")
    print(url)
