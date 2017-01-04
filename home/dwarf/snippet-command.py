import gdb

class MyCommand(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, "command_tester", gdb.COMMAND_NONE)

    def invoke (self, args, from_tty):
        print("args: {}".format(args))

        print("args well splited: {}".format(args))
        for i, arg in enumerate(gdb.string_to_argv(args)):
            print("{}) {}".format(i, arg))
            
MyCommand() # don't forget to instanciate your object
