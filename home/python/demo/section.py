import gdb

# https://sourceware.org/gdb/current/onlinedocs/gdb/Breakpoints-In-Python.html#Breakpoints-In-Python
    
class StartStopBreakpoint(gdb.Breakpoint):
    def __init__(self, loc, section_bpt, is_start):
        gdb.Breakpoint.__init__(self, loc, internal=True)
        self.silent = True
        
        self.is_start = is_start
        self.section_bpt = section_bpt
        
    def stop(self):
        self.section_bpt.in_section = self.is_start
        # and/or
        self.section_bpt.enabled = not self.is_start
        
        return False # never stop here
        
class SectionBreakpoint(gdb.Breakpoint):
    def __init__(self, location):
        gdb.Breakpoint.__init__(self, location, internal=True)
        self.silent = True
        self.in_section = False
        
    def stop(self):
        if self.in_section:
            return False # ignore hit in section
        else:
            print("Section breakpoint hit outside of section")

            def double_check(): # just to be sure ...
                main_frame = gdb.newest_frame().older()
                if main_frame.read_var("i") != main_frame.read_var("bad"):
                    print("---> i != bad ??? :(")
                    
            double_check()

            sal = gdb.newest_frame().find_sal()
            print("Stopped in {}:{}".format(sal.symtab,sal.line))
            gdb.execute("list {},{}".format(sal.line, sal.line)) # prints only the current line
            return True # hit outside of section, do stop

class BreakSection_cmd(gdb.Command):
    def __init__ (self):
        gdb.Command.__init__(self, "break_section", gdb.COMMAND_OBSCURE)
        
    def invoke (self, args, from_tty):
        start, stop, run = args.split(" ")

        section_bpt = SectionBreakpoint(run)
        StartStopBreakpoint(start, section_bpt, is_start=True)
        StartStopBreakpoint(stop,  section_bpt, is_start=False)
        
        print("Section breakpoint set on start={} stop={} run={}".format(start, stop, run))

BreakSection_cmd()
