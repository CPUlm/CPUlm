from lib_carotte import *
allow_ribbon_logic_operations(True)

WITH_MUL = False
WITH_DIV = False


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
    return incr(~a)


def mul(a, b):
    assert(a.bus_size == b.bus_size)
    n = a.bus_size
    zn = Constant("0"*n)

    result = zn
    c = Constant("0")
    for i in range(n):
        ajout = mux(a[i], zn, b)
        result,c_i = n_adder(result, ajout)
        b = b[1:n] + Constant("0")
        c = c | c_i
        
    return (result,c)


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

        dividende_rogne = dividende_rogne + dividende[n-i-1]                    # le nouveau dividende
        trop_court = or_n_bits(diviseur[i+1:n]) if i+1 != n else Constant("0")  # indique si il n'y a pas assez de bits pour faire la soustraction
        neg_div,_ = negation(diviseur[0:i+1])                                   
        diff,_ = n_adder(dividende_rogne, neg_div)                              # resultat si on fait la soustraction

        plus_grand = (~trop_court) & diff[diff.bus_size-1]   # indique si il y a assez de bits et que le resultat de la soustraction est positif

        quotient = quotient + plus_grand
        dividende_rogne = mux(plus_grand, dividende_rogne, diff)
    return quotient


def main():
    rs1 = Input(32)
    rs2 = Input(32)
    alucode = Input(3)
    rs2_neg,rs2_neg_carry = negation(rs2)

    rd_and = rs1 & rs2
    rd_or = rs1 | rs2
    rd_nor = ~rd_or
    rd_xor = rs1 ^ rs2
    rd_add,c_add = n_adder(rs1, rs2)
    rd_sub,c_sub = n_adder(rs1, rs2_neg)
    rd_mul,c_mul = mul(rs1, rs2) if WITH_MUL else rs1,Constant("0")
    rd_div = div(rs1, rs2) if WITH_DIV else rs1

    rd = mux_n(alucode[0:3], (rd_and, rd_or, rd_nor, rd_xor, rd_add, rd_sub, rd_mul, rd_div))


    flag_z = ~or_n_bits(rd)
    flag_n = rd[rd.bus_size-1]
    flag_c = mux_n(alucode[0:3], (Constant("0"), Constant("0"), Constant("0"), Constant("0"), c_add, c_sub, c_mul, Constant("0")))
    signe_rs1 = rs1[rs1.bus_size - 1]
    signe_rs2 = rs2[rs2.bus_size - 1]
    signe_rs2_neg = rs2_neg[rs2.bus_size - 1]
    signe_rd = rd[rd.bus_size - 1]

    flag_v = mux_n(alucode[0:3], (Constant("0"),
                                  Constant("0"),
                                  Constant("0"),
                                  Constant("0"),
                                  (signe_rs1^signe_rs2) | ((~signe_rs1)^signe_rd),  # addition : il y a overflow si les nombre que l'on additionne sont de même signe et que le résultat n'est pas du même signe
                                  rs2_neg_carry | (signe_rs1 ^ signe_rs2_neg) | ((~signe_rs1)^signe_rd),  # soustratction : de même mais avec le nombre négatif associé 
                                  Constant("0"),
                                  Constant("0")))

    
    rd.set_as_output("rd")
    flag_z.set_as_output("flag_z")
    flag_n.set_as_output("flag_n")
    flag_c.set_as_output("flag_c")
    flag_v.set_as_output("flag_v")
