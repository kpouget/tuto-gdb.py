import gdb

# https://sourceware.org/gdb/current/onlinedocs/gdb/Breakpoints-In-Python.html#Breakpoints-In-Python
    
class StartStopBreakpoint(gdb.Breakpoint):
    def __init__(self, loc, section_bpt, is_start):
        gdb.Breakpoint.__init__(self, loc, internal=True)
        self.silent = True
        ...
        
    def stop(self):
        ...
        
        return False # never stop here
        
class SectionBreakpoint(gdb.Breakpoint):
    def __init__(self, location):
        gdb.Breakpoint.__init__(self, location, internal=True)
        self.silent = True
        ...
        
    def stop(self):
        ...


class BreakSection_cmd(gdb.Command):
    def __init__ (self):
        gdb.Command.__init__(self, "break_section", gdb.COMMAND_OBSCURE)
        
    def invoke (self, args, from_tty):
        start, stop, run = args.split(" ")

        # ...
        
        print("Section breakpoint set on start={} stop={} run={}".format(start, stop, run))

BreakSection_cmd()
