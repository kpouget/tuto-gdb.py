import pkgutil, sys
import logging as log

import gdb

import my_gdb
import my_gdb.archi as archi

# package type --> implementation
current_impls = {}
# package type --> (list of implementations)
impls_list = {}


VOID = None
VOID_P = None
VOID_PP = None
CHAR = None
CHAR_P = None
CHAR_PP = None
INT = None
INT_P = None
INT_108A = None
ULONG = None
UINT = None

def initialize_archi():
    """
    Initializes the target stack (access, archi and system).
    Look into the three submodules, and initialize them.
    """
    
    for ttype in [archi]:
        prefix = ttype.__name__ + "."
        type_name = ttype.__name__.split(".")[-1]
        impls_list[ttype] = {}
        for importer, impl_name, ispkg in pkgutil.iter_modules(ttype.__path__, prefix):
            try:
                impl = sys.modules[impl_name]
                impl_name = impl_name.split(".")[-1]
                log.info("Found target %s.%s", type_name, impl_name)
                
                impl.init(my_gdb)
                impls_list[ttype][impl_name] = impl
            except KeyError as ke:
                pass
            except Exception as e:
                log.warn("Couldn't load target %s (%s)", impl_name, e)
        
        current_impls[ttype] = ttype.prefered

def initialize_types():
    """
    Initialize types global variables with common types.
    """
    global VOID, VOID_P, VOID_PP
    global CHAR, CHAR_P, CHAR_PP
    global INT, INT_P, INT_108A
    global ULONG, UINT
    
    VOID = gdb.lookup_type("void")
    VOID_P = VOID.pointer()
    VOID_PP = VOID_P.pointer()
    
    CHAR = gdb.lookup_type("char")
    CHAR_P = CHAR.pointer()
    CHAR_PP = CHAR_P.pointer()
    
    INT = gdb.lookup_type("int")
    INT_P = INT.pointer()
    INT_108A = INT.array(108)

    UINT = gdb.lookup_type("unsigned int")
    ULONG = gdb.lookup_type("unsigned long")
    
def first_arg(ttype=None):
    return nth_arg(1, ttype)

def second_arg(ttype=None):
    return nth_arg(2, ttype)

def third_arg(ttype=None):
    return nth_arg(3, ttype)

def fourth_arg(ttype=None):
    return nth_arg(4, ttype)

def nth_arg(n, ttype=None):
    try:
        frame = gdb.selected_frame()
        arg = [e for e in frame.block() if e.is_argument][n-1] # hello
        ret = gdb.selected_frame().read_var(arg)
    except IndexError:
        ret = get_target(archi).nth_arg(n, ttype)
    except RuntimeError: #Cannot locate block for frame.
        ret = get_target(archi).nth_arg(n, ttype)
        
    if ret is None:
        raise IndexError("Architecture '%s' could't return %dth argument" %
                         (get_target(archi).__name__), n)
    
    return ret

def return_value(ttype=None):
    return get_target(archi).return_value(ttype)

def return_regname():
    return get_target(archi).return_regname()

def read_value(where, ttype=None):
    """
    Reads the memory location `where` with type `ttype`.

    :param where: location to read
    :param ttype: C type of `where`. Default: void *
    """
    ttype = VOID_P if ttype is None else ttype

    frame = gdb.selected_frame()
    if where.startswith("$"):
        return frame.read_register(where[1:]).cast(ttype)
    else:
        to_parse = "(%s) %s" % (str(ttype), where)
        return gdb.parse_and_eval(to_parse)

def load_types_on_first_new_objfile(evt):
    gdb.events.new_objfile.disconnect(load_types_on_first_new_objfile)
    initialize_types()

def get_target(ttype):
    """
    Returns the relevant implementation for the target type asked.
    :param ttype: archi, system or access submodule.
    :returns: the relevant implementation of the asked type.
    """
    
    if ttype == archi:
        str_archi = gdb.execute("show architecture", to_string=True) 
        if current_impls[archi].recognize(str_archi):
            return current_impls[archi]
        else:
            for impl in impls_list[ttype].values():
                if impl.recognize(str_archi):
                    current_impls[archi] = impl
                    return impl
            else:
                log.exception("No architecture found for '%s'", 
                              str_archi)
            
    return current_impls[ttype]

def initialize():
    gdb.events.new_objfile.connect(load_types_on_first_new_objfile)
    initialize_archi()
    
initialize()
