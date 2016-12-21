import gdb

SILENT_STEPS = True

def addr2num(addr):
    try:
        return int(addr)  # Python 3
    except:
        return long(addr) # Python 2
    
def callstack_depth():
    depth = 1
    frame = gdb.newest_frame()
    while frame is not None:
        frame = frame.older()
        depth += 1
    return depth


class StepBeforeNextCall (gdb.Command):
    def __init__ (self):
        super (StepBeforeNextCall, self).__init__ ("step-before-next-call",
                                                   gdb.COMMAND_OBSCURE)

    def invoke (self, arg, from_tty):
        arch = gdb.selected_frame().architecture()

        while True:
            ...

        print("step-before-next-call: next instruction is a call.")
        print("{}: {}".format(hex(int(disa["addr"])), disa["asm"]))

class StepIntoNextCall (gdb.Command):
    def __init__ (self):
        super (StepIntoNextCall, self).__init__ ("step-into-next-call", 
                                               gdb.COMMAND_OBSCURE)

    def invoke (self, arg, from_tty):
        start_depth = current_depth = callstack_depth()

        # step until we're one step deeper
        while ...: ...

        # display information about the two top frames
        print("Stepped into function {}\n".format(gdb.newest_frame().name()))
        gdb.execute("frame 0")
        gdb.execute("frame 1")


StepIntoNextCall() 
StepBeforeNextCall()
