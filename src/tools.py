from constants import *

def assert_same_type(a, b):
    if isinstance(a, tuple) or isinstance(b, tuple):
        assert (len(a) == len(b))
        for (u,v) in zip(a,b):
            assert_same_type(u,v)
    
    elif (not isinstance(a, tuple)) and (not isinstance(b, tuple)):
        assert(a.bus_size == b.bus_size)
    else:
        assert(False)



def incr(a):
    # TODO
    return a

def mux_jmp(opcode, not_jmp, is_jmp):
    # Peut être facilement ameliore
    assert_same_type(not_jmp, not_jmp)
    return mux_opcode(opcode, not_jmp, not_jmp, not_jmp, is_jmp)

def mux_alu(opcode, not_alu, is_alu):
    # Peut être facilement ameliore
    assert_same_type(not_alu, is_alu)
    return mux_opcode(opcode, is_alu, not_alu, not_alu, not_alu)

def mux_opcode(opcode, alu, shift, load_store, jmp):
    # TODO
    return alu
