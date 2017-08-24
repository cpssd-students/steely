'''
.slag <person in chat>

slags a person in the chat
'''


import random


__author__ = 'devoxel'
COMMAND='.slag'
REPLIES = (
    "{} smells like a baby prostitute",
    "{}, you whore",
    "Shut up {}",
    "Nice wig, {}. What's it made of?",
    "{}, I would unplug your life support to charge my phone",
    "{}, I wonder if you'd be able to speak more clearly if your parents were seconds cousins instead of first",
    "{}, you are impossible to understimate",
    "I'd insult {} behind their back but my cars only got half a tank of gas",
    "{} you absolute walnut",
    "{} you stupid fucking almond",
    "{}, you like that you fucking pecan?",
    "Whoever is willing to fuck {} is just too lazy to masturbate.",
    "Everyone who has ever loved {} was wrong",
    "{}, I hope you outlive your children",
    "{}, you're a fuckin muppet",
    "{}, you're as dumb as a mule and twice as ugly. If a strange man offers you a ride, I say take it.",
    "{}, go play in traffic",
    "{} you are a fucking overdeveloped cumshot. GET OUT OF MY SIGHT.",
)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    # NOTE: could validate name. easier if i dont tho lol
    name = message.strip()
    if not name:
        bot.sendMessage("cant even type a command correctly jfc",
            thread_id=thread_id, thread_type=thread_type)
        return
    bot.sendMessage(random.choice(REPLIES).format(name),
        thread_id=thread_id, thread_type=thread_type)
