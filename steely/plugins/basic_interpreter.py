'''
Evaluate BASIC, or something vaguely similar looking.

Usage: .basic <source_code>

Example:
UncleBob:
    .basic
    10 PRINTLN counter
    20 LET counter = counter + 1
    30 IF counter < 5 THEN GOTO 10
    40 PRINTLN "Done"
Chat Bot:
    0
    1
    2
    3
    4
    Done

Each line must follow the format of:
    LABEL INSTRUCTION ARG1 ARG2...

Variables are 32 signed bit ints and can be named any string that doesn't
include whitespace. They don't need to be declared, they are implicitly set to
0 on their first usage.

Execution starts at the lowest valued label and works its way up to the
highest. Execution finishes when the highest value label is exectued.
(Provided it does not jump back to an earlier label).

There are a number of instructions.

PRINT ...:
    Prints a variable or a string if enclosed in quotes.
    Eg:
    10 PRINT my_var
    20 PRINT " is the value of my_var"
    Output:
    0 is the value of my_var

PRINTLN ...:
    The same as PRINT but with a newline at the end.

IF ... THEN GOTO ...:
    Conditional statement, allows for the following comparisons.
    =, <>, <, >, >=, <=.
    If the statement matches execution continues at the given label. Otherwise
    continuing to the next largest label as usual.
    Variables or constants can be used in the comarison.
    Eg:
    10 IF counter > 5 THEN GOTO 30

LET ... = ...:
    Assignment statment, allows mutation of variables.
    There is two forms, simple assignment:
    10 LET A = 3
    20 LET B = A
    Or assignment of the result of a calculation:
    10 LET A = A + 1
    20 LET B = A / 7
    The following operations are supported:
    +, -, *, /.


There are no tests lol.
Based on code for the Kattis problem:
https://open.kattis.com/problems/basicinterpreter
'''

__author__ = "cianlr"
import operator
import threading
import traceback
from collections import defaultdict


COMMAND = 'basic'


class BasicInterpreter:
    def __init__(self, stdout=print, stderr=print):
        self._stdout = stdout
        self._stderr = stderr
        self.is_kill = False
        self._cur_instr = None
        self._vars = defaultdict(int)
        self._instrs = {}
        self._label_chain = {None: None}
        self._val_op_handlers = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.floordiv,
        }
        self._cond_op_handlers = {
            '=': operator.eq,
            '>': operator.gt,
            '<': operator.lt,
            '<>': operator.ne,
            '<=': operator.le,
            '>=': operator.ge,
        }
        # Each instruction takes one argument, its args as a list.
        # They are responsible for incrementing the instruction counter
        # themselves
        self._instr_handlers = {
            'LET': self._instr_LET,
            'IF': self._instr_IF,
            'PRINT': self._instr_PRINT,
            'PRINTLN': self._instr_PRINTLN,
        }

    def _next_instr(self):
        return self._label_chain[self._cur_instr]

    def _get_var(self, val):
        if val.isdigit():
            return int(val)
        else:
            return self._vars[val]

    def _32_bit_wrap(self, n):
        return ((n + 2147483648) % (4294967296)) - 2147483648

    def _instr_PRINT(self, args):
        if '"' in args:
            self._stdout(args.strip('"'))
        else:
            self._stdout(str(self._vars[args.strip()]))
        self._cur_instr = self._next_instr()

    def _instr_PRINTLN(self, args):
        self._instr_PRINT(args)
        self._stdout('\n')

    def _instr_LET(self, args):
        args = args.split()
        if len(args) == 3:
            assign, _, var = args
            self._vars[assign] = self._get_var(var)
        else:
            assign, _, var1, op, var2 = args
            self._vars[assign] = self._32_bit_wrap(
                    self._val_op_handlers[op](
                        self._get_var(var1),
                        self._get_var(var2)))
        self._cur_instr = self._next_instr()

    def _instr_IF(self, args):
        var1, op, var2, _, _, t_next = args.split()
        if self._cond_op_handlers[op](self._get_var(var1),
                                      self._get_var(var2)):
            self._cur_instr = int(t_next)
        else:
            self._cur_instr = self._next_instr()

    def add_instructions(self, instructions):
        for line in instructions:
            if not line:
                continue
            label, instr, args = line.strip().split(' ', 2)
            self._instrs[int(label)] = (instr, args)
        label_order = sorted(self._instrs)
        self._label_chain = {l: next_l for l, next_l in zip(
            [None] + label_order,
            label_order + [None])}

    def loop(self):
        self._cur_instr = self._next_instr()
        while self._cur_instr != None and not self.is_kill:
            inst, args = self._instrs[self._cur_instr]
            self._instr_handlers[inst](args)

    def try_loop(self):
        try:
            self.loop()
        except Exception as e:
            self._stderr("Exception on instruction {}: {}\n".format(
                str(self._cur_instr), repr(e)))
            self._stderr(traceback.format_exc())


THREAD_TIMEOUT = 1
MAX_OUTPUT = 1500


def main(bot, author_id, source_code, thread_id, thread_type, **kwargs):
    def send(message):
        bot.sendMessage(str(message), thread_id=thread_id, thread_type=thread_type)

    global stdout
    stdout = ''
    def add_stdout(s):
        global stdout
        stdout += s

    global stderr
    stderr = ''
    def add_stderr(s):
        global stderr
        stderr += s

    try:
        bi = BasicInterpreter(stdout=add_stdout, stderr=add_stderr)
        bi.add_instructions(source_code.strip().split('\n'))
    except Exception as error:
        send("There was an error parsing your code. "
             "Ensure it's in the format: LINE# INSTR ARG1 ARG2...")
        send(str(error))
        return

    thread = threading.Thread(target=bi.try_loop)
    thread.start()
    thread.join(timeout=THREAD_TIMEOUT)
    if thread.is_alive():
        send("Your thread hit the {}s timeout".format(THREAD_TIMEOUT))
        bi.is_kill = True
        return

    if stderr:
        send("STDERR: " + stderr)

    if len(stdout) > MAX_OUTPUT:
        send(stdout[:MAX_OUTPUT] + '\nOutput trimmed to' + str(MAX_OUTPUT))
    else:
        send(stdout)
