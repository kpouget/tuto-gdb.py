import gdb
import logging as log

gdb.execute("source common.py")
import my_gdb

class RegWatch_cmd(gdb.Command):
    def __init__ (self):
        gdb.Command.__init__(self, "reg_watch", gdb.COMMAND_OBSCURE)
        
    def invoke (self, args, from_tty):
        try:
            args = args.split(" ")
            reg, fct = args[:2]
            format = " ".join(args[2:])
            
        except Exception:
            print("Usage: reg_watch register function [format]")
            return

        try:
            if not gdb.lookup_symbol(fct)[0]:
                print("Error: cannot find symbol '{}'".format(fct))
                return
        except gdb.error: # No frame selected.
            print("Error: Please start the execution before setting reg watchpoints")
            return
                
        disa = gdb.execute("disassemble {}".format(fct), to_string=True)

        watchpoints = []
        for line in disa.replace("=> ", "").split("\n"):
            addr, _, rest = line.strip().partition(" ")

            if not "%{}".format(reg) in rest:
                continue

            watchpoints.append(RegWatch_bpt(addr, line, reg[1:], format))

        print("{} watchpoints added in function {}".format(len(watchpoints), fct))

class RegWatch_bpt(gdb.Breakpoint):
    def __init__(self, addr, line, reg, format):
        gdb.Breakpoint.__init__(self, "*{}".format(addr), internal=True)
        self.silent = True
        self.line = line
        self.reg = reg
        self.format = format
        
    def stop(self):
        # before_val = str(gdb.newest_frame().read_register(self.reg))
        before_val = gdb.parse_and_eval("({}) ${}".format(self.format, self.reg))
        
        print("before: ({}) {}".format(self.format, before_val))
        print(self.line)
        def after():
            gdb.execute("nexti", to_string=True)
            # after_val = str(gdb.newest_frame().read_register(self.reg))
            after_val = gdb.parse_and_eval("({}) ${}".format(self.format, self.reg))
            
            if after_val == before_val: after_val = "<unchanged>"
            else: after_val = "({}) {}".format(self.format, after_val)
            
            print("after:  {}".format(after_val))

        my_gdb.before_prompt(after)
        
        return True


RegWatch_cmd()
