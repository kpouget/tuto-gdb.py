import gdb

def before_prompt(fct):
     old_prompt = gdb.prompt_hook
     def prompt(prompt):
        try:
            fct()
        except Exception as e:
            log.warn("Before prompt function {} failed: {}".format(fct, e))
            log.info(e)
        gdb.prompt_hook = old_prompt
        return old_prompt(prompt) if old_prompt else prompt
     
     gdb.prompt_hook = prompt

class FunctionBreakpoint(gdb.Breakpoint):
    breakpointed = {}
    stop_requests = []

    def __init__ (self, spec):
        gdb.Breakpoint.__init__ (self, spec, internal=True)
        self.silent = True

    def stop (self):
        ret = self.prepare_before()
        
        if ret is None:  #spurious stop
            return False

        (fct_stop, fct_finish, fct_data) = ret

        if fct_finish:
            FunctionFinishBreakpoint(self, fct_data)

        while FunctionBreakpoint.stop_requests:
            print(FunctionBreakpoint.stop_requests.pop())
            fct_stop = True

        return fct_stop

    def prepare_before(self):
        return None

    def prepare_after(self, data):
        return False

    @classmethod
    def push_stop_request(clazz, msg):
        clazz.stop_requests.append(msg)

class FunctionFinishBreakpoint (gdb.Breakpoint):
    def __init__ (self, parent, fct_data):
        gdb.Breakpoint.__init__(self, "*%s" % gdb.newest_frame().older().pc(), internal=True)
        #gdb.FinishBreakpoint.__init__(self, "*%s" % gdb.newest_frame(), internal=True) # too slow in last versions
        self.silent = True
        self.parent = parent
        self.fct_data = fct_data

    def stop(self):
        self.enabled = False

        fct_stop = self.parent.prepare_after(self.fct_data)

        gdb.post_event(self.delete)

        while FunctionBreakpoint.stop_requests:
            print(FunctionBreakpoint.stop_requests.pop())
            fct_stop = True

        return fct_stop

    def out_of_scope(self):
        pass


