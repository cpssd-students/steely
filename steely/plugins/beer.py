from steely import config
import requests

# steely stuff
__author__ = 'devoxel'
COMMAND = '.beer'

# API stuff
URL = 'http://api.brewerydb.com/v2/'
SEARCH = URL + "search/"
API_KEY = config.BREWERYDB_API_KEY

# error stuff
ERR_NO_RESULTS = "ah now we got no results"
ERR_API_LIMIT = "we used up all our api juice, try again tomorrow"
ERR_WHAT = "no idea whats going on"

def search_request(q):
    payload = {
        'q': q,
        'type': 'beer',
        'key': API_KEY,
    }
    r = requests.get(SEARCH, params=payload)
    if r.status_code != 200:
        raise ValueError
    return r.json()

def format_output(r):
    if 'data' not in r:
        return ERR_NO_RESULTS
    beer = r['data']
    if len(beer) == 0:
        return ERR_NO_RESULTS

    # just take the first result
    beer = beer[0]
    output_format = [
            ('{}', ['nameDisplay']),
            ('abv: {}%', ['abv']),
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

    img_url = None
    if 'labels' in beer:
        img_url = beer['labels']['medium']

    return '\n'.join(out), img_url

def searcher(query):
    try:
        q = search_request(query)
    except ValueError:
        return ERR_API_LIMIT
    return format_output(q)

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    desc, url = searcher(message)
    if not desc:
        bot.sendMessage(ERR_WHAT, thread_id=thread_id, thread_type=thread_type)
    if url:
        bot.sendRemoteImage(url, thread_id=thread_id, thread_type=thread_type)
    bot.sendMessage(desc, thread_id=thread_id, thread_type=thread_type)

if __name__ == "__main__":
    import sys
    desc, url = searcher(sys.argv[1])
    print(desc)
    print("---")
    print(url)
