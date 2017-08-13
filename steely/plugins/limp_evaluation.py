'''
Evaluate limp, a lisp-flavoured language.

Usage: .limp <source_code> 

### Example 1###
UncleBob: ".limp (+ 2 3)"
Chat Bot: "5"

### Example 2###
UncleBob: ".limp (// 100 (- 5 2))"
Chat Bot: "33"

For more information on how to write limp code, see https://www.github.com/byxor/limp
Perhaps you feel like contributing to the language! I welcome anything (relevant) that has been fully covered by automatic tests and doesn't limit the architecture.
'''


import limp


COMMAND = '.limp'


def main(bot, author_id, message, thread_id, thread_type, **kwargs):

    def send(text):
        bot.sendMessage(text, thread_id=thread_id, thread_type=thread_type)

    def sendError(error):
        send("Sorry, you have an error: {}".format(error))
        
    source_code = message
    try:
        result = limp.evaluate(source_code)
    except (SyntaxError, NameError) as e:
        sendError(e)
    except Exception as e:
        send("Something unexpected happened: {}".format(e))
        send("Please inform Brandon, thanks.")
