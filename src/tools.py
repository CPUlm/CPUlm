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
    if t.bus_size == 1:
        return mux(t,v[0],v[1])
    else:
        cas1 = mux_n(t[0:t.bus_size-1], v[0:mil])
        cas2 = mux_n(t[0:t.bus_size-1], v[mil:n])
        res = mux(t[t.bus_size-1], cas1, cas2)
        return res

def mux_jmp(opcode, not_jmp, is_jmp):
    #return mux_opcode(opcode, not_jmp, not_jmp, not_jmp, is_jmp)
    assert_same_type(not_jmp, is_jmp)
    vaut7 = opcode[0] & opcode[1] & opcode[2]
    ok = opcode[3] | vaut7
    return mux(ok, not_jmp, is_jmp)

def mux_alu(opcode, not_alu, is_alu):
    assert_same_type(not_alu, is_alu)
    return mux(opcode[0] | opcode[1] | opcode[2] | opcode[3], is_alu, not_alu)

def mux_alu_shift_load(opcode, alu, shift, load_store):
    return mux(opcode[2], mux(opcode[0] | opcode[1], alu, shift), load_store)

def mux_opcode(opcode, alu, shift, load_store, jmp):
    as_or_lj = opcode[2] | opcode[3]
    s = opcode[0] | opcode[1]
    j = opcode[3] | (opcode[0] & opcode[1] & opcode[2])
    
    cas1 = mux(s, alu, shift)
    cas2 = mux(j, load_store, jmp)
    return mux(as_or_lj, cas1, cas2)

### addition et incrementation ###
def incr(a):
    assert(a.bus_size >= 1)
    s = ~a[0]
    c = a[0]
    for i in range(1, a.bus_size-1):
        s_i = a[i] ^ c
        c = a[i] & c
        s = s + s_i
    s_i = a[a.bus_size-1] ^ c
    s = s + s_i
    assert_same_type(a, s)
    return s

def full_adder(a, b, c):
    tmp = a ^ b
    return (tmp ^ c, (tmp & c) | (a & b))

def n_adder_carry(a, b, c):
    assert(a.bus_size == b.bus_size)
    (s, c) = full_adder(a[0], b[0], c) # Treat the 0 case separately since variables have a bus size >= 1
    for i in range(1, a.bus_size):
        (s_i, c) = full_adder(a[i], b[i], c)
        s = s + s_i
    return (s, c)

def n_adder(a,b):
    return n_adder_carry(a,b,Constant("0"))

def one_hot(a):
    m = a.bus_size
    res = mux(a[0], Constant("01"), Constant("10"))
    
    for i in range(1,m):
        assert(res.bus_size == 2**i)
        zn = Constant("0"*(2**i))
        res = mux(a[i], res+zn, zn+res)
    assert(res.bus_size == 2**m)
    return res
