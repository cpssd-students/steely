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
import limp.environment


COMMAND = '.limp'


def main(bot, author_id, source_code, thread_id, thread_type, **kwargs):
    def send(x):
        bot.sendMessage(str(x), thread_id=thread_id, thread_type=thread_type)

    def sendError(info, error):
        _full_error_message = '{type(error).__name__}: {str(error)}'
        send(f'{info}: {_full_error_message}')

    try:
        environment = environment.create_standard()
        environment['send'] = send
        result = limp.evaluate(source_code, environment)
        send(result)
    except (SyntaxError, NameError) as error:
        sendError('You have an error', error)
    except Exception as error:
        sendError('Something unexpected happened', error)
        send('It\'s possible that it\'s your fault.')

