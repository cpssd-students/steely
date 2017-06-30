import json
import requests

COMMAND = '.dbus'

BASE_URL = "http://data.dublinked.ie/cgi-bin/rtpi/"
def get_stop_routes(stop_id):
  url = BASE_URL + "busstopinformation?stopid={}&format=json".format(stop_id)
  res = requests.get(url).json()
  routes = []
  for r in res["results"]:
    for ops in r['operators']:
      routes.extend(ops['routes'])
  return routes

def next_bus_realtime(stop_id, routes):
  url = BASE_URL + "realtimebusinformation?stopid={}&format=json".format(stop_id)
  base_str_format = "{} should arrive in {} mins, heading to {}\n"
  res = requests.get(url).json()
  done = []
  busses = ""
  try: 
    for arrival in res['results']:
      if arrival['route'] not in done:
        done.append(route)
        busses = busses + base_str_format.format(arrival['route'],
                                                 arrival['duetime'],
                                                 arrival['destination'])
    return busses
  except (TypeError, KeyError):
    return "no results"
    

  
  

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
  if not message:
    bot.sendMessage("please include a stop number", thread_id=thread_id, thread_type=thread_type)
  else:
    try:
      bot.sendMessage(next_bus_realtime(message, get_stop_routes(message)), thread_id=thread_id, thread_type=thread_type)
    except requests.exceptions.RequestException:
      bot.sendMessage("error retrieving results", thread_id=thread_id, thread_type=thread_type)
    
