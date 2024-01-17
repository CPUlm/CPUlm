from lib_carotte import *
allow_ribbon_logic_operations(True)

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


### addition et incrementation ###
def incr(a):
    assert(a.bus_size >= 1)
    c = a[0]
    s = ~a[0]
    for i in range(1, a.bus_size):
        s_i = a[i] ^ c
        c = a[i] & c
        s = s + s_i
    assert_same_type(a, s)
    return (s,c)

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

def negation(a):
    r=~a
    return incr(~a)



def or_n_bits(a):
    r = a[0]
    for i in range(1, a.bus_size):
        r = r | a[i]
    return r


def div(dividende, diviseur):
    # il s'agit de l'algorithme de division standard (celui qu'on pose à la main)
    # on considère donc de plus en plus de bits du quotient, et on soustrait le diviseur quand c'est possible
    assert(dividende.bus_size == diviseur.bus_size)
    n = dividende.bus_size

    # comme il est impossible d'initialiser les variables à Constant(""), ces quelques lignes simulent la première itération de la boucle
    dividende_rogne = dividende[n-1]
    trop_court = or_n_bits(diviseur[1:n])   # les seuls nombre restants possibles sont 0 (on ignore) et 1 (on suppose donc qu'on divise par 1)
    plus_grand = (~trop_court) & dividende_rogne
    quotient = plus_grand
    dividende_rogne = mux(plus_grand, dividende_rogne, Constant("0"))

    for i in range(1,n):
        assert (dividende_rogne.bus_size == i)
        assert (quotient.bus_size == i)
        #  on va faire l'étape où le dividende a i+1 bits
        #  on a donc déjà calculé les i premiers bits du quotient

        dividende_rogne = dividende[n-i-1] + dividende_rogne                   # le nouveau dividende
        trop_court = or_n_bits(diviseur[i+1:n]) if i+1 != n else Constant("0")  # indique si il n'y a pas assez de bits pour faire la soustraction
        neg_div,_ = negation(diviseur[0:i+1])                                   
        diff,carry_neg = n_adder(dividende_rogne, neg_div)                              # resultat si on fait la soustraction

        plus_grand = (~trop_court) & (carry_neg)   # indique si il y a assez de bits et que le resultat de la soustraction est positif

        quotient = plus_grand + quotient 
        dividende_rogne = mux(plus_grand, dividende_rogne, diff)
    assert(quotient.bus_size == dividende.bus_size)
    return quotient


def main():
    rs1 = Input(32)
    rs2 = Input(32)
    rd_div = div(rs1, rs2)

    
    rd_div.set_as_output("rd")
