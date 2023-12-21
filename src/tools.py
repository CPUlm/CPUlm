from constants import *

### assert ###

def assert_same_type(a, b):
    if (isinstance(a, tuple) and isinstance(b, tuple)) or (isinstance(a,list) and isinstance(b,list)):
        assert (len(a) == len(b))
        for (u,v) in zip(a,b):
            assert_same_type(u,v)
    elif isinstance(a,tuple) or isinstance(b,tuple) or isinstance(a,list) or isinstance(b,list):
        assert(False)
    else:
        assert(a.bus_size == b.bus_size)




### manipulation des registres ###

def get_reg(id_reg, regs):
    return mux_n(id_reg, ( Constant("0"*WORD_SIZE), Constant("0"*(WORD_SIZE-1)+"1")) + regs)

def update_regs(regs_old, id_reg, regVal):
    arr = [regs_old, regs_old]

    for i in range(len(regs_old)):
        deb = regs_old[0:i]
        fin = regs_old[i+1:len(regs_old)]
        arr.append( deb + (regVal,) + fin)

    return mux_n(id_reg, arr)





### flags ###

def test_flags(flags, flagsMask):
    f0 = Mux(flagsMask[0], Constant("0"), flags[0])
    f1 = Mux(flagsMask[1], Constant("0"), flags[1])
    f2 = Mux(flagsMask[2], Constant("0"), flags[2])
    f3 = Mux(flagsMask[3], Constant("0"), flags[3])
    return ( (f0 | f1) | (f2 | f3) )




### MUX specifiques ###    

def mux(m, a, b):
    # pareil que MUX(m,a,b), mais a et b peuvent etre des tuples (donc remplace MUX)
    assert_same_type(a, b)
    if not isinstance(a, tuple):
        return Mux(m, a, b)
    
    result = []
    for (u,v) in zip(a,b):
        result.append(mux(m, u, v))
    return tuple(result)


def mux_n(t,v):
    n = len(v)
    mil = n//2
    assert(n == 2**t.bus_size)
    if t.bus_size <= 1:
        return v[0]
    else:
        cas1 = mux_n(t[1:t.bus_size], v[0:mil])
        cas2 = mux_n(t[1:t.bus_size], v[mil:n])
        res = mux(t[0], cas1, cas2)
        return res

def mux_jmp(opcode, not_jmp, is_jmp):
    assert_same_type(not_jmp, not_jmp)
    vaut7 = opcode[0] & opcode[1] & opcode[2]
    ok = opcode[3] | vaut7
    return mux(ok, not_jmp, is_jmp)

def mux_alu(opcode, not_alu, is_alu):
    assert_same_type(not_alu, is_alu)
    return mux(opcode[0] | opcode[1] | opcode[2] | opcode[3], is_alu, not_alu)

def mux_opcode(opcode, alu, shift, load_store, jmp):
    as_or_lj = opcode[0] | opcode[1]
    s = opcode[2] | opcode[3]
    j = opcode[0] | (~opcode[1] & ~opcode[2] & ~opcode[3])
    
    cas1 = mux(s, alu, shift)
    cas2 = mux(j, load_store, jmp)
    return mux(as_or_lj, cas1, cas2)


### addition et incrementation ###
def incr(a):
    assert(a.bus_size >= 1)
    c = Constant("1")
    s = ~a[0]
    c = a[0]
    for i in range(1, a.bus_size):
        s_i = a[i] ^ c
        c = a[i] & c
        s = s + s_i
    assert_same_type(a, s)
    return s

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

