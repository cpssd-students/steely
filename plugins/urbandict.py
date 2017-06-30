import requests

COMMAND = '.ud'

def define(term):
    results = []
    term = '+'.join(term.split())
    r = requests.get('http://api.urbandictionary.com/v0/define?term=' + term)
    if r.json()['result_type'] != 'exact':
        return results
    for result in r.json()['list']:
        results.append({'definition':result['definition'], 'example':result['example']})
    return results

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    definitions = define(message)
    if not message or not definitions:
        bot.sendMessage('no results', thread_id=thread_id, thread_type=thread_type)
        return
    text = 'Definition: ' + definitions[0]['definition'] + '\nExample: ' + definitions[0]['example']
    bot.sendMessage(text, thread_id=thread_id, thread_type=thread_type)
    
