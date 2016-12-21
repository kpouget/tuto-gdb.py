import gdb

from .. import my_archi

my_gdb = None

ARG_REG_PREFIX = "w"

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
    
    return my_archi.read_value("${}{}".format(ARG_REG_PREFIX, n-1), ttype)

def return_value(ttype):
    """
    Gets the cased value returned by the last function call.

    :param ttype: type to which we cast the value read.
    :returns: the value returned by the last function call.
    """

    return nth_arg(1, ttype)

###############

def recognize(str_archi):
    return "aarch64" in str_archi
