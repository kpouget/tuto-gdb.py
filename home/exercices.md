Scripting `gdb.py`
==================

Preliminary setup
-----------------

Prepare and launch the docker container:

    HOST_DIR=/home/kevin/jdd_debug_data/ # absolute path required
    docker run -it -v $HOST_DIR:/home/jcf/host -e GROUPID=$(id -g) -e USERID=$(id -u) --cap-add sys_ptrace kpouget/tuto-gdb.py

Then if you want to share the data with your host, work from `~/host`, otherwise stay in `~`:

    cd ~/host # if you want to share the data with your host
    
Prepare the binaries:

    cd dwarf/
    make
    cd ..
    cd python
    make

Discovering gdb-cli and gdb.py
------------------------------

Start GDB:

    cd dwarf
    gdb prodconsum
    start

Go somewhere:

    tbreak consumer
    # stopped in a consumer thread
    continue

    # go to main thread
    thread 1
    # go to main frame
    up

And now we play with gdb-cli:

    print context
    ptype context
    print &context

And now we play with gdb.py. 
`pp` is a custom command I made, it means python-print: `pi print(args)`. 
`ppd` is also a custom command, it means pyton-print-dir: `pi print(dir(args))`

    pp gdb.parse_and_eval("context")
    ppd gdb.parse_and_eval("context")

Now we enter Python mode:

    pi # or python-interactive
    ctx = gdb.parse_and_eval("context")
    ctx # <gdb.Value object at 0x7f1a91af3970> # ctx is a Python object abstracting the `context` variable:

    err = ctx['error'] # <gdb.Value object at 0x7f1a91af38f0>
    print(err)

Let's look at the types

    print(err.type) # type int
    dir(err.type) # sizeof
    print(err.type.sizeof)
    print(err.type.pointer()) # type int *
    
Let's play with some values:

    # go back to the thread that hit the breakpoint
    (gdb) info threads
    (gdb) thread 3 # in my case

Then, back in pyton mode (`pi`):

    _ctx = gdb.parse_and_eval("_context")
    print(_ctx) # 0x7ffe6172f9f0
    print(_ctx.type) # void *

Let's check the code:

    gdb.execute("list") # to see the cod
    122	void* consumer(void* _context){
    123	        puts("in consumer");
    124	        struct Context* context = (struct Context*)_context;


Variable `_context` is `void *`, that makes sense. But we can cast it into a `struct Context*`:

    ctx_type = gdb.lookup_type("struct Context *") # doesn't work
    ctx_type = gdb.lookup_type("struct Context") # works !
    ctx_ptr_type = ctx_type.pointer()
    print(ctx_ptr_type) # struct Context * # yes !
    
    ctx = _ctx.cast(ctx_ptr_type).dereference()
    print(ctx) # yes !


Just to try:

     gdb.execute("set scheduler-locking on") # don't run anything else meanwhile
     gdb.parse_and_eval("puts")("Hello world !")
     gdb.execute("set scheduler-locking off")

A few other things:

     gdb.execute("disassemble main")
     for line in gdb.execute("disassemble main", to_string=True).split("\n"):
         if 'callq' in line: print(line[:-1])

     # or
     frame = gdb.selected_frame()
     frame.architecture().disassemble(frame.read_register("pc"))
     frame.architecture().disassemble(int(frame.read_register("pc")))
     frame.architecture().disassemble(int(frame.read_register("pc"))+4)
     frame.architecture().disassemble(int(frame.read_register("pc"))+4*2+3)
     # [{'length': 5, 'asm': 'callq  0x4008f0 <pthread_mutex_lock@plt>', 'addr': 4197358}]


Hooking into gdb.py
-------------------

We far we've seem you to run Python code in GDB cli, but not really how to script it. 
Let's give it a try. Save the following code snippets into a file, and `source` them from GDB:

      (gdb) source snippet-_____.py

First, we need new commands to interact with the user (`dwarf/snippet-command.py`):

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

We also need ways to trigger code execution, for instance on breakpoints (`dwarf/snippet-breakpoint.py`):

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
    
            print("Stopped with i == 5.")
            print("Letters sent by the producer so far:")
            data = gdb.newest_frame().read_var("data") # type Value<char[]>
            for idx in range(int(i)):
                print("{}: {}".format(idx, chr(data[idx])))
    
            return True # stop now

    MyBreakpoint() # don't forget to instanciate your object

Finally, we'll try to insert code on gdb execution events (`dwarf/snippet-events.py`):

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

Try to run different processes with this debugger script and see how it behaves. To get a StopEvent that is not a BreakpointEvent, try:

    (gdb) start
    ...
    (gdb) print sleep(5)
    ^C
    Program received signal SIGINT, Interrupt.
    0x00007f312b916fe0 in __nanosleep_nocancel () from /usr/lib/libc.so.6
    STOP: program stopped because of a SignalEvent
    ...
    
Now you're know the basics of GDB scripting ! Get back to the slides *Part 2*, to try to build new commands with real utilities!
The program is:

1. Section breakpoint
2. Return true breakpoint
3. Register watchpoint
4. Step into next call
5. Faking function execution