###############
import logging as log

import gdb
gdb.execute("source common.py")

import my_gdb
import my_gdb.my_archi

class FunctionReturnBreakpoint(my_gdb.FunctionBreakpoint):
    def __init__ (self, fct, expected):
        my_gdb.FunctionBreakpoint.__init__(self, fct)

        self.expected = expected
        
    def prepare_before(self):
        return (False, # don't stop here
                True,  # stop at return to execute self.prepare_after
                {})    # don't transmit anything to prepare_after::data

    def prepare_after(self, data):
        if not self.expected: # no expected value, so stop anyway
            return True

        ret = my_gdb.my_archi.return_value(self.expected.type) # cast return value to its expected type
        
        log.info("Test {} return value ({}) against expected value ({})".format(self.location, ret, self.expected))
        do_stop = ret == self.expected

        if do_stop:
            print("\nStopped after finding '{}' return value = {} in {}.".format(self.location, ret, my_gdb.my_archi.return_regname()))
            gdb.execute("where 1") # prints the current frame

        return do_stop

class BreakReturn_cmd(gdb.Command):
    def __init__ (self):
        gdb.Command.__init__(self, "break_return", gdb.COMMAND_OBSCURE)
        
    def invoke (self, args, from_tty):
        fct, _, val = args.partition(" ")

        value = gdb.parse_and_eval(val) if val else None

        FunctionReturnBreakpoint(fct, value)

        print("Breakpoint set on function '{}' if it returns '{}'".format(fct, val))

BreakReturn_cmd()
