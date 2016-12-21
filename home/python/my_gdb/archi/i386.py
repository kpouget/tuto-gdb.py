import gdb

from .. import my_archi

my_gdb = None

def init(my_gdb_pkg):
    global my_gdb
    my_gdb = my_gdb_pkg

def get_sp_above():
    """
    (internal)
    :returns: the stack pointer of the frame above
    :rtype: gdb.Value
    """
    frame = gdb.selected_frame()
    frame.older().select()
    sp = gdb.parse_and_eval("$sp")
    frame.select()
    return sp

def nth_arg(n, ttype):
    """
    Gets the casted value of the nth argument of the selected frame.
    
    :param n: index of the parameter to return.
    :param ttype: type to which we cast the value read. Default: void *
    :returns: the value of the nth argument of the currently selected frame.
    :rtype: gdb.Value
    """
    
    ttype = my_archi.VOID_P if ttype is None else ttype
    argAddr = get_sp_above() + (n-1) * 4
    
    return argAddr.cast(ttype.pointer()).dereference()
    
def return_value(ttype):
    """
    Gets the cased value returned by the last function call.

    :param ttype: type to which we cast the value read.
    :returns: the value returned by the last function call.
    """
    return my_archi.read_value("$eax", ttype)

def return_regname():
    return "$eax"

###############

def recognize(str_archi):
    return "automatically" in str_archi and "(currently i386)" in str_archi
