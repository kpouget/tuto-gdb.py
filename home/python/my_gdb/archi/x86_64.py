import gdb

from .. import my_archi

my_gdb = None

arg_regs = ("$rax", "$rdi", "$rsi", "$rdx", "$rcx", "$r8", "$r9")

def init(my_gdb_pkg):
    global my_gdb 
    my_gdb = my_gdb_pkg
    
def nth_arg(n, ttype):
    """
    Gets the casted value of the nth argument of the selected frame.
    
    :param n: index of the parameter to return.
    :param ttype: type to which we cast the value read. Default: void *
    :returns: the value of the nth argument of the currently selected frame.
    :rtype: gdb.Value
    """
    
    if n < len(arg_regs):
        return my_archi.read_value(arg_regs[n], ttype)
    else:
        return stack_nth_arg(n, ttype)

def stack_nth_arg(n, ttype):
    assert n >= len(arg_regs)
    
    n -= len(arg_regs) 
    
    sp = get_sp_above(ttype)
    argAddr = sp + n 
    
    return argAddr.dereference()

def return_value(ttype):
    """
    Gets the cased value returned by the last function call.

    :param ttype: type to which we cast the value read.
    :returns: the value returned by the last function call.
    """
    
    return nth_arg(0, ttype)

def return_regname():
    return arg_regs[0]

def get_sp_above(ttype=None):
    """
    (internal)
    :returns: the stack pointer of the frame above
    :rtype: gdb.Value
    """
    frame = gdb.selected_frame()
    frame.older().select()
    
    cast = ("(%s) " % ttype.pointer()) if ttype is not None else "" 
    
    sp = gdb.parse_and_eval(cast+"$sp")
    frame.select()
    return sp

###############

def recognize(str_archi):
    return "automatically" in str_archi and "(currently i386:x86-64)" in str_archi
