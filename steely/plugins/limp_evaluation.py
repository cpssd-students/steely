'''
Evaluate limp, a lisp-flavoured language.

Usage: .limp <source_code>

# example 1
UncleBob: ".limp (+ 2 3)"
Chat Bot: "5"

# example 2
UncleBob: ".limp (// 100 (- 5 2))"
Chat Bot: "33"

For more information on how to write limp code, see https://www.github.com/byxor/limp
Perhaps you feel like contributing to the language!
I welcome anything (relevant) that has been fully covered by automatic tests and doesn't limit the architecture.
'''


import limp


COMMAND = '.limp'


def main(bot, author_id, source_code, thread_id, thread_type, **kwargs):
    def send(text):
        bot.sendMessage(text, thread_id=thread_id, thread_type=thread_type)

    try:
        result = limp.evaluate(source_code)
        send(result)
    except (SyntaxError, NameError) as error:
        send(f'you have an error: {error}')
    except Exception as error:
        send(f'something unexpected happened: {error}')
        send('please inform Brandon')
