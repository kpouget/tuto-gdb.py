# no end-of-window enter-key-to-continue
set height 0 
set width 0

# for docker
set disable-randomization off

set breakpoint pending on

# conveniant to debug python code
set python print-stack full

# may not be compatible with
set confirm off 

# structures are not displayed inline
set print pretty 

# yes !
set history filename ~/host/.gdb_history
set history save 

# New commands for Python:
# (gdb) pp py_obj
# <> print(str(py_obj)) ...
#
# (gdb) ppd py_obj
# <> print(dir(py_obj))

python
import gdb

class pp(gdb.Command):
        """Python print its args"""
        def __init__(self):
                gdb.Command.__init__ (self, "pp", gdb.COMMAND_DATA, completer_class=gdb.COMPLETE_SYMBOL)

        def invoke (self, arg, from_tty):
                gdb.execute("python(print(%s))" % arg) # do it in GDB python env, not here
pp()

class ppd(gdb.Command):
        """Python print dir() of its args"""
        def __init__(self):
                gdb.Command.__init__ (self, "ppd", gdb.COMMAND_DATA, completer_class=gdb.COMPLETE_SYMBOL)

        def invoke (self, arg, from_tty):
                gdb.execute("python(print(dir(%s)))" % arg) # do it in GDB python env, not here
ppd()
end
