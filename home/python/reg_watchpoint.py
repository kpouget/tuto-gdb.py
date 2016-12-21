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
                ...
        except gdb.error: # No frame selected.
            ...
                
        disa = gdb.execute("disassemble {}".format(fct), to_string=True)
        # => 0x0000000000466d50 <+0>:	sub    $0x28,%rsp
        #    0x0000000000466d54 <+4>:	movq   $0x0,(%rsp)
        #    ...

        watchpoints = []
        for line in disa.replace("=> ", "").split("\n"):
            addr, _, rest = line.strip().partition(" ")
            ...

        print("{} watchpoints added in function {}".format(len(watchpoints), fct))

class RegWatch_bpt(gdb.Breakpoint):
    def __init__(self, addr, line, reg, format):
        gdb.Breakpoint.__init__(self, "*{}".format(addr), internal=True)
        self.silent = True
        
        self.line = line
        self.reg = reg
        self.format = format
        
    def stop(self):
        before_val = gdb.parse_and_eval("({}) ${}".format(self.format, self.reg))

        ...
        
        def after():
            ...
            
            if after_val == before_val: after_val = "<unchanged>"
            else: after_val = "({}) {}".format(self.format, after_val)
            
            ...

        my_gdb.before_prompt(after) # because we can't `nexti` from gdb.Breakpoint.stop callback
        
        return True # always stop here, to trigger before_prompt callback


RegWatch_cmd()
