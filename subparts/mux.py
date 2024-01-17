from lib_carotte import *
allow_ribbon_logic_operations(True)

### MUX specifiques ###    

def mux(m, a, b):
    # pareil que MUX(m,a,b), mais a et b peuvent etre des tuples (donc remplace MUX)
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

def main():
    a = Input(2)
    b = mux_n(a, (Constant("00"), Constant("01"), Constant("10"), Constant("11")))
    b.set_as_output("b")
