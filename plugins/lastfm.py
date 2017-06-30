import requests
from .. import config

COMMAND = '.np'

def get_np(apikey, user):
  base = "http://ws.audioscrobbler.com/2.0/"
  url = "?method=user.getrecenttracks&user={}&api_key={}&limit=2&format=json"\
                  .format(user, apikey)
  res = requests.get(base+url)
  print(res.json())
  return res.json()["recenttracks"]["track"][0]
  

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
  if not message:
    bot.sendMessage('include username please', thread_id=thread_id, thread_type=thread_type)
  else:
   try:
      np = get_np(LASTFM_API_KEY, message)
      artist = np['artist']['#text']
      song = np['name']
      bot.sendMessage('{} is playing {} by {}'.format(message, song, artist),
                       thread_id=thread_id, thread_type=thread_type)
   except requests.exceptions.RequestException as e:
     bot.sendMessage('failed to retrieve now playing information',
                     thread_id=thread_id, thread_type=thread_type)
     print(e)

      
    
  
