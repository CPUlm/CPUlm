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

def mux_tuple(m, a, b):
    assert_same_type(a, b)
    if not isinstance(a, tuple):
        return Mux(m, a, b)
    
    result = []
    for (u,v) in zip(a,b):
        result.append(mux_tuple(m, u, v))
    return tuple(result)

def get_reg(regId, regs):
    # TODO adapter a plus de 4 regs
    return Mux(regId[0],
            Mux(regId[2], regs[0], regs[2]),
            Mux(regId[2], regs[1], regs[3]))

def update_regs(regs_old, id_reg, regVal):
    # TODO adapter a plus de 4 reg
    result2 = (regVal, regs_old[1], regs_old[2], regs_old[3])
    result3 = (regs_old[0], regVal, regs_old[2], regs_old[3])
    result4 = (regs_old[0], regs_old[1], regVal, regs_old[3])
    result5 = (regs_old[0], regs_old[1], regs_old[2], regVal)
    return mux_tuple(id_reg[0],
            mux_tuple(id_reg[2], result2, result4),
            mux_tuple(id_reg[2], result3, result5))

def test_flags(flags, flagsMask):
    f0 = Mux(flagsMask[0], Constant("0"), flags[0])
    f1 = Mux(flagsMask[1], Constant("0"), flags[1])
    f2 = Mux(flagsMask[2], Constant("0"), flags[2])
    f3 = Mux(flagsMask[3], Constant("0"), flags[3])
    return ( (f0 | f1) | (f2 | f3) )
    
def full_adder(a, b, c):
    tmp = a ^ b
    return (tmp ^ c, (tmp & c) | (a & b))

def n_adder(a, b):
    assert(a.bus_size == b.bus_size)
    c = Constant("0")
    (s, c) = full_adder(a[0], b[0], c) # Treat the 0 case separately since variables have a bus size >= 1
    for i in range(1, a.bus_size):
        (s_i, c) = full_adder(a[i], b[i], c)
        s = s + s_i
    return (s, c)

def incr(a):
    n = a.bus_size
    (s,c) = n_adder(a, Constant("0"*(n-1) + "1"))
    return s

def mux_jmp(opcode, not_jmp, is_jmp):
    # Peut être facilement ameliore
    assert_same_type(not_jmp, not_jmp)
    return mux_opcode(opcode, not_jmp, not_jmp, not_jmp, is_jmp)

def mux_alu(opcode, not_alu, is_alu):
    # Peut être facilement ameliore
    assert_same_type(not_alu, is_alu)
    return mux_opcode(opcode, is_alu, not_alu, not_alu, not_alu)

def mux_opcode(opcode, alu, shift, load_store, jmp):
    as_or_lj = opcode[0] | opcode[1]
    s = opcode[2] | opcode[3]
    j = opcode[0] | (~opcode[1] & ~opcode[2] & ~opcode[3])
    
    cas1 = mux_tuple(s, alu, shift)
    cas2 = mux_tuple(j, load_store, jmp)
    return mux_tuple(as_or_lj, cas1, cas2)
