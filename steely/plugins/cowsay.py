import textwrap
import random

__author__ = ('Smurphicus')
COMMAND = 'cowsay'

animals = [
"""
\  ^__^
 \ (oo)\_______
   (__)\       )\/\\
       ||----w |
       ||     ||
"""
,
"""
    \   .--.
     \ |o_o |
       |:_/ |
      //   \\ \\
     (|     | )
    /'\\_   _/`\\
    \\___)=(___/
"""
,
"""
 \    / <`     '> \\
  \  (  / @   @ \  )
      \(_ _\_/_ _)/
    (\ `-/     \-' /)
     "===\     /==="
      .==')___(`==.
       .='     `=.
"""
,
"""
\      .~~,
 \ ,_-( 9  )
     '-'==( ___\)
       ( (   . /
        \\ '-` /
         '-j~`
         :="
"""
]

def normalize_text(str):
    lines = textwrap.wrap(str, 24)
    return [line.ljust(len(max(lines, key=len))) for line in lines]

def get_border(line_count,index):
    if line_count == 1:
        return [ "<", ">" ]

    elif index == 0:
        return [ "/", "\\" ]

    elif index == line_count - 1:
        return [ "\\", "/" ]

    else:
        return [ "|", "|" ]


def bubble_message(text):
    bubble = []

    normalized_text = normalize_text(text)

    border_size = len(normalized_text[0])

    bubble.append("  " + "_" * border_size)

    for index, line in enumerate(normalized_text):
        border = get_border(len(normalized_text), index)

        bubble.append("%s %s %s" % (border[0], line, border[1]))

    bubble.append("  " + "-" * border_size)

    return "\n".join(bubble)

def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    cow_message = bubble_message(message) + random.choice(animals)
    bot.sendMessage(cow_message, thread_id=thread_id, thread_type=thread_type)
