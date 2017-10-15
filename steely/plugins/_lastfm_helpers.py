from requests_futures.sessions import FuturesSession
from steely import config
from tinydb import TinyDB, Query
import requests


COMMAND = '.np'
USERDB = TinyDB('databases/lastfm.json')
USER = Query()
SESSION = FuturesSession(max_workers=100)
API_BASE = "http://ws.audioscrobbler.com/2.0/"
COLLAGE_BASE = "http://www.tapmusic.net/collage.php/"
SHORTENER_BASE = 'https://www.googleapis.com/urlshortener/v1/url'
PERIODS = ("7day", "1month", "3month", "6month", "12month", "overall")
REQUEST_PARAMETERS = {'api_key': config.LASTFM_API_KEY,
		      'format': 'json'}


def get_lastfm_request(method, **kwargs):
    ''' make a normal python request to the last.fm api
        return a Response() '''
    return requests.get(API_BASE, params={"method": method,
                                          **REQUEST_PARAMETERS,
                                          **kwargs})


def get_lastfm_asyncrequest(method, **kwargs):
    ''' make an aysnc request using a requests_futures FuturesSession
        to the last.fm api
        return a Future() '''
    return SESSION.get(API_BASE, params={"method": method,
                                          **REQUEST_PARAMETERS,
                                          **kwargs})


def get_lastfm_asyncrequest_list(method, **kwargs):
    ''' call get_lastfm_asyncrequest for each user '''
    for user in USERDB.all():
        username = user["username"]
        yield get_lastfm_asyncrequest(method,
            user=username, limit=1, **kwargs)
