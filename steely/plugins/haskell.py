# External Dependencies:
# - firejail (for sandboxing)


from subprocess import Popen, PIPE, STDOUT


COMMAND = "haskell"
__doc__ = "Compiles and executes Haskell."
__author__ = "byxor"


TIMEOUT_IN_SECONDS = 10
TIMEOUT_MESSAGE = "Request timed out. Don't be naughty."


SCRIPT = "plugins/_haskell.sh"
SHELL_COMMAND = ["firejail", "timeout", f"{TIMEOUT_IN_SECONDS}", "bash", SCRIPT]


def main(bot, author_id, code, thread_id, thread_type, **kwargs):
    bot.sendMessage(attempt_to_run(code), thread_id=thread_id, thread_type=thread_type)


def attempt_to_run(code):
    result = run(code)
    if timed_out(result):
        return TIMEOUT_MESSAGE
    return result


def run(code):
    process = Popen(SHELL_COMMAND, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    encoding = "utf-8"
    code_bytes = code.encode(encoding)
    write_code_to_process = lambda: process.communicate(input=code_bytes)
    output = write_code_to_process()[0].decode(encoding)
    return output


def timed_out(result):
    return (SCRIPT in result) and ("Terminated" in result)
