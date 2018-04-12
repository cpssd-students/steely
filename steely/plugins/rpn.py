'''
Evaluate an expression in reverse polish notation.
'''


import rpn


__author__ = 'sentriz'
COMMAND = 'rpn'


def main(bot, author_id, source_code, thread_id, thread_type, **kwargs):
    def send(message):
        bot.sendMessage(str(message), thread_id=thread_id,
                        thread_type=thread_type)

    def send_error(info, error):
        full_error_message = f'{type(error).__name__}: {error}'
        send(f'{info} {full_error_message}')
    try:
        send(rpn.solve(source_code))
    except (SyntaxError, NameError, TypeError) as error:
        send_error('you got a', error)
    except Exception as error:
        send_error('hmmm', error)
