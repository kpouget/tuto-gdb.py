import gdb

def exit_handler(exited_event):
    try:
        print("EXITED: program terminated with code  {}".format(exited_event.exit_code))
    except AttributeError:
        # Variable: ExitedEvent.exit_code
        # An integer representing the exit code, if available, which the inferior has returned.
        # (The exit code could be unavailable if, for example, gdb detaches from the inferior.)
        # If the exit code is unavailable, the attribute does not exist.
        print("EXITED: program detached (no return code)")
        
def new_objfile_handler(objfile_event):
    print("NEW_OBJFILE: program loaded a library: {}".format(objfile_event.new_objfile.filename))

def stop_handler(stop_event):
    print("STOP: program stopped because of a {}".format(stop_event.__class__.__name__))

gdb.events.exited.connect(exit_handler)
gdb.events.new_objfile.connect(new_objfile_handler)
gdb.events.stop.connect(stop_handler)

