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


import rpn


COMMAND = '.rpn'


def main(bot, author_id, source_code, thread_id, thread_type, **kwargs):
    def send(message):
        bot.sendMessage(str(message), thread_id=thread_id, thread_type=thread_type)
    def send_error(info, error):
        full_error_message = f'{type(error).__name__}: {error}'
        send(f'{info} {full_error_message}')
    try:
        send(rpn.solve(source_code))
    except (SyntaxError, NameError, TypeError) as error:
        send_error('you got a', error)
    except Exception as error:
        send_error('hmmm', error)
