import gdb

# (gdb) list prodconsum.c:104
# 102	        int i;
# 103	        for(i = 0; i < sizeof(data); i++){
# 104	                if(!context->error){

class MyBreakpoint(gdb.Breakpoint):
    def __init__ (self):
        gdb.Breakpoint.__init__(self, "prodconsum.c:104",
                                internal=True)
        self.silent = True
        print("Custom breakpoint on {} set.".format(self.location))

    def stop(self):
        i = gdb.parse_and_eval("i") # type Value<int>
        
        if int(i) != 9:
            return False # don't stop

        print("Stopped with i == 9.")

        print("Letters sent by the producer so far:")

        data = gdb.newest_frame().read_var("data") # type Value<char[]>
        for idx in range(int(i)):
            print("{}: {}".format(idx, chr(data[idx])))

        return True # stop now

MyBreakpoint()
