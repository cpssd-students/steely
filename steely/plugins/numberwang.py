"""
gimme a number and see what happens
"""

import random

__author__ = 'devoxel'
COMMAND = 'nw'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def numberwang():
	random.choice( ["NUMBERWANG!", 
					"Another one",
					"Thaaaaaat's Numberwang!",
					"Okay", "Uh huh", 
					"WangerNumb ;)"
					],
					 weights = [3, 20, 2, 20, 20, 1])

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
	if is_number(message):
		bot.sendMessage(numberwang(), thread_id=thread_id, thread_type=thread_type)
		return
	s = "G'way with that sort of thing."
    bot.sendMessage(s, thread_id=thread_id, thread_type=thread_type)
