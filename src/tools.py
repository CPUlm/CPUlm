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
    return mux5bits(regId, Constant("0"*WORD_SIZE), Constant("0"*(WORD_SIZE-1)+"1"), regs[0], regs[1], regs[2], regs[3], regs[4], regs[5], regs[6], regs[7], regs[8], regs[9], regs[10], regs[11], regs[12], regs[13], regs[14], regs[15], regs[16], regs[17], regs[18], regs[19], regs[20], regs[21], regs[22], regs[23], regs[24], regs[25], regs[26], regs[27], regs[28], regs[29])


def update_regs(regs_old, id_reg, regVal):
    # TODO adapter a plus de 4 reg
    r0 = (regs_old[0], regs_old[1], regs_old[2], regs_old[3], regs_old[4], regs_old[5], regs_old[6], regs_old[7], regs_old[8], regs_old[9], regs_old[10], regs_old[11], regs_old[12], regs_old[13], regs_old[14], regs_old[15], regs_old[16], regs_old[17], regs_old[18], regs_old[19], regs_old[20], regs_old[21], regs_old[22], regs_old[23], regs_old[24], regs_old[25], regs_old[26], regs_old[27], regs_old[28], regs_old[29])

    r2 = (regVal, regs_old[1], regs_old[2], regs_old[3], regs_old[4], regs_old[5], regs_old[6], regs_old[7], regs_old[8], regs_old[9], regs_old[10], regs_old[11], regs_old[12], regs_old[13], regs_old[14], regs_old[15], regs_old[16], regs_old[17], regs_old[18], regs_old[19], regs_old[20], regs_old[21], regs_old[22], regs_old[23], regs_old[24], regs_old[25], regs_old[26], regs_old[27], regs_old[28], regs_old[29])

    return mux5bits(id_reg, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0, r0)

def test_flags(flags, flagsMask):
    f0 = Mux(flagsMask[0], Constant("0"), flags[0])
    f1 = Mux(flagsMask[1], Constant("0"), flags[1])
    f2 = Mux(flagsMask[2], Constant("0"), flags[2])
    f3 = Mux(flagsMask[3], Constant("0"), flags[3])
    return ( (f0 | f1) | (f2 | f3) )

def mux5bits(t, v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31):
    t0 = t[0]
    t1 = t[1]
    t2 = t[2]
    t3 = t[3]
    t4 = t[4]
    return mux_tuple(t0, mux_tuple(t1, mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v0, v1),
                                                                   mux_tuple(t4, v2, v3)),
                                                     mux_tuple(t3, mux_tuple(t4, v4, v5),
                                                                   mux_tuple(t4, v6, v7))),
                                       mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v8, v9),
                                                                   mux_tuple(t4, v10, v11)),
                                                     mux_tuple(t3, mux_tuple(t4, v12, v13),
                                                                   mux_tuple(t4, v14, v15)))),
                         mux_tuple(t1, mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v16, v17),
                                                                   mux_tuple(t4, v18, v19)),
                                                     mux_tuple(t3, mux_tuple(t4, v20, v21),
                                                                   mux_tuple(t4, v22, v23))),
                                       mux_tuple(t2, mux_tuple(t3, mux_tuple(t4, v24, v25),
                                                                   mux_tuple(t4, v26, v27)),
                                                     mux_tuple(t3, mux_tuple(t4, v28, v29),
                                                                   mux_tuple(t4, v30, v31)))))
    
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
