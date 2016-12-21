###############
import logging as log

gdb.execute("source common.py")

import my_gdb
import my_gdb.my_archi

class SkipFunctionBreakpoint(gdb.Breakpoint):
    def __init__ (self, fct):
        gdb.Breakpoint.__init__(self, fct, internal=True)
        self.silent = True
        
    def stop(self):
        gdb.execute("return")
        return False
    

class SkipFunction_cmd(gdb.Command):
    def __init__ (self):
        gdb.Command.__init__(self, "skip_function", gdb.COMMAND_OBSCURE)
        
    def invoke (self, args, from_tty):
        SkipFunctionBreakpoint(args)

        print("Skip breakpoint set on function '{}'".format(args))

SkipFunction_cmd()

###############################

class FakeRunFunctionBreakpoint(gdb.Breakpoint):
    def __init__ (self):
        gdb.Breakpoint.__init__(self, "run", internal=True)
        self.silent = True
        
    def stop(self):
        i = int(gdb.newest_frame().read_var("i"))
        if i % 10 == 0:
            gdb.execute("call bug({})".format(i))
            
        gdb.execute("return")
        return False

class FakeRunFunction_cmd(gdb.Command):
    def __init__ (self):
        gdb.Command.__init__(self, "fake_run_function", gdb.COMMAND_OBSCURE)
        
    def invoke (self, args, from_tty):
        FakeRunFunctionBreakpoint()

        print("Fake function run execution".format(args))

FakeRunFunction_cmd()
