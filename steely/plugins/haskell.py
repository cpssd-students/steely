# External Dependencies:
# - firejail (for sandboxing)
# - ghc (for compiling haskell)


from subprocess import Popen, PIPE, STDOUT


COMMAND = "haskell"
__doc__ = "Compiles and executes Haskell."
__author__ = "byxor"



SHELL_COMMAND = ["bash", "plugins/_haskell.sh"]


def main(bot, author_id, code, thread_id, thread_type, **kwargs):
    bot.sendMessage(run(code), thread_id=thread_id, thread_type=thread_type)


def run(code):
    process = Popen(SHELL_COMMAND, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    encoding = "utf-8"
    code_bytes = code.encode(encoding)
    write_code_to_process = lambda: process.communicate(input=code_bytes)
    output = write_code_to_process()[0].decode(encoding)
    return output
