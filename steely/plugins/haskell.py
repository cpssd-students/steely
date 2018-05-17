# External Dependencies:
# - firejail (for sandboxing)


from subprocess import Popen, PIPE, STDOUT
from threading import Timer


COMMAND = "haskell"
__doc__ = "Compiles and executes Haskell."
__author__ = "byxor"


SHELL_COMMAND = ["firejail", "bash", "plugins/_haskell.sh"]
TIMEOUT_IN_SECONDS = 10


def main(bot, author_id, code, thread_id, thread_type, **kwargs):
    bot.sendMessage(attempt_to_run(code), thread_id=thread_id, thread_type=thread_type)


def attempt_to_run(code):
    result = run(code)
    if result is not None:
        return result
    return "Request timed out. Don't be naughty."


def run(code):
    process = Popen(SHELL_COMMAND, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    timer = Timer(TIMEOUT_IN_SECONDS, process.kill)
    try:
        timer.start()
        return communicate(process, code)
    finally:
        timer.cancel()


def communicate(process, code):
    encoding = "utf-8"
    code_bytes = code.encode(encoding)
    write_code_to_process = lambda: process.communicate(input=code_bytes)
    output = write_code_to_process()[0].decode(encoding)
    return output
