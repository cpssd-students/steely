'''.sentiment tracks user positivity or negativity in previous message for all the autismos'''
import requests
import json
COMMAND = '.sentiment'


def get_sentiment(string):
	response = requests.post("http://text-processing.com/api/sentiment/", "text=" + string)
	data = response.json()
	body = "The phrase you've checked is '" + string + "'.\n"
	body += "We're " + str(int(round((data['probability']['pos'] * 100), 2))) + "% sure the message is positive\n" 
	body += "We're " + str(int(round((data['probability']['neg'] * 100), 2))) + "% sure the message is negative\n" 
	body += "We're " + str(int(round((data['probability']['neutral'] * 100), 2))) + "% sure the message is neutral\n"
	if str(data['label']) == "pos":
		body += "I'm gonna guess this shit is positive."
	elif str(data['label']) == "neg":
		body += "I'm gonna guess this shit is negative."
	else:
		body += "I'm gonna guess this shit is neutral."

	return body

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(get_sentiment(message.text), thread_id=thread_id, thread_type=thread_type)
