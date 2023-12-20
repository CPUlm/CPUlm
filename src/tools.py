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


def get_reg(id_reg, regs):
    #return mux5bits(id_reg, ( Constant("0"*WORD_SIZE), Constant("0"*(WORD_SIZE-1)+"1")) + regs, regs[0], regs[1], regs[2], regs[3], regs[4], regs[5], regs[6], regs[7], regs[8], regs[9], regs[10], regs[11], regs[12], regs[13], regs[14], regs[15], regs[16], regs[17], regs[18], regs[19], regs[20], regs[21], regs[22], regs[23], regs[24], regs[25], regs[26], regs[27], regs[28], regs[29])
    return mux5bits(id_reg, ( Constant("0"*WORD_SIZE), Constant("0"*(WORD_SIZE-1)+"1")) + regs)


def update_regs(regs_old, id_reg, regVal):
    arr = [regs_old, regs_old]

    for i in range(len(regs_old)):
        deb = regs_old[0:i]
        fin = regs_old[i+1:len(regs_old)]
        arr.append( deb + (regVal,) + fin)

    return mux5bits(id_reg, arr)

def test_flags(flags, flagsMask):
    f0 = Mux(flagsMask[0], Constant("0"), flags[0])
    f1 = Mux(flagsMask[1], Constant("0"), flags[1])
    f2 = Mux(flagsMask[2], Constant("0"), flags[2])
    f3 = Mux(flagsMask[3], Constant("0"), flags[3])
    return ( (f0 | f1) | (f2 | f3) )

def mux5bits(t, v):
    t0 = t[0]
    t1 = t[1]
    t2 = t[2]
    t3 = t[3]
    t4 = t[4]
    return mux_tuple(t0, mux_tuple(t1, mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v[0], v[1]),
                                                                   mux_tuple(t4, v[2], v[3])),
                                                     mux_tuple(t3, mux_tuple(t4, v[4], v[5]),
                                                                   mux_tuple(t4, v[6], v[7]))),
                                       mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v[8], v[9]),
                                                                   mux_tuple(t4, v[10], v[11])),
                                                     mux_tuple(t3, mux_tuple(t4, v[12], v[13]),
                                                                   mux_tuple(t4, v[14], v[15])))),
                         mux_tuple(t1, mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v[16], v[17]),
                                                                   mux_tuple(t4, v[18], v[19])),
                                                     mux_tuple(t3, mux_tuple(t4, v[20], v[21]),
                                                                   mux_tuple(t4, v[22], v[23]))),
                                       mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v[24], v[25]),
                                                                   mux_tuple(t4, v[26], v[27])),
                                                     mux_tuple(t3, mux_tuple(t4, v[28], v[29]),
                                                                   mux_tuple(t4, v[30], v[31])))))
    
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
    assert_same_type(not_jmp, not_jmp)
    vaut7 = opcode[0] & opcode[1] & opcode[2]
    ok = opcode[3] | vaut7
    return mux_tuple(ok, not_jmp, is_jmp)

def mux_alu(opcode, not_alu, is_alu):
    assert_same_type(not_alu, is_alu)
    return mux_tuple(opcode[0] | opcode[1] | opcode[2] | opcode[3], is_alu, not_alu)

def mux_opcode(opcode, alu, shift, load_store, jmp):
    as_or_lj = opcode[0] | opcode[1]
    s = opcode[2] | opcode[3]
    j = opcode[0] | (~opcode[1] & ~opcode[2] & ~opcode[3])
    
    cas1 = mux_tuple(s, alu, shift)
    cas2 = mux_tuple(j, load_store, jmp)
    return mux_tuple(as_or_lj, cas1, cas2)
