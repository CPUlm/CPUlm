from constants import *
from tools import *


def mul(a, b):
    assert(a.bus_size == b.bus_size)
    n = a.bus_size

    or_lst = [b[n-1]]
    for i in range(1,n-1):
        new_or = or_lst[0] | b[n-i-1]
        or_lst.insert(0,new_or)
    # or_lst[i] contient or_n_bits(b[i+1:n])

    result = b[0] & a[n-1]
    c = a[n-1] & or_lst[0]
    for i in range(1,n):
        assert(result.bus_size == i)
        result = Constant("0") + result
        result_si_ajout,c_i = n_adder(result, b[0:i+1])
        if i+1 < n:
            c_i = c_i | or_lst[i]
        result = mux(a[n-i-1], result, result_si_ajout)
        c = mux(a[n-i-1],c, c|c_i)
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

    or_lst = [diviseur[n-1]]
    for i in range(1,n-1):
        new_or = or_lst[0] | diviseur[n-i-1]
        or_lst.insert(0,new_or)
    # or_lst[i] contient or_n_bits(diviseur[i+1:n])

    # comme il est impossible d'initialiser les variables à Constant(""), ces quelques lignes simulent la première itération de la boucle
    dividende_rogne = dividende[n-1]
    trop_court = or_lst[0]   # les seuls nombre restants possibles sont 0 (on ignore) et 1 (on suppose donc qu'on divise par 1)
    plus_grand = (~trop_court) & dividende_rogne
    quotient = plus_grand
    dividende_rogne = mux(plus_grand, dividende_rogne, Constant("0"))

    for i in range(1,n):
        assert (dividende_rogne.bus_size == i)
        assert (quotient.bus_size == i)
        #  on va faire l'étape où le dividende a i+1 bits
        #  on a donc déjà calculé les i premiers bits du quotient

        dividende_rogne = dividende[n-i-1] + dividende_rogne                   # le nouveau dividende
        trop_court = or_lst[i] if i+1 != n else Constant("0")  # indique si il n'y a pas assez de bits pour faire la soustraction
        diff,carry_neg = n_adder_carry(dividende_rogne, ~diviseur[0:i+1], Constant("1"))                              # resultat si on fait la soustraction

        plus_grand = (~trop_court) & (carry_neg)   # indique si il y a assez de bits et que le resultat de la soustraction est positif

        quotient = plus_grand + quotient 
        dividende_rogne = mux(plus_grand, dividende_rogne, diff)
    assert(quotient.bus_size == dividende.bus_size)
    return quotient


def alu(instruction, rs1, rs2):
    alucode = instruction[OPCODE_BITS + 3*REG_BITS : OPCODE_BITS + 3*REG_BITS + ALU_BITS]
    
    add_or_sub = alucode[0]
    rs2_to_add = mux(add_or_sub,rs2,~rs2)

    rd_and = rs1 & rs2
    rd_or = rs1 | rs2
    rd_nor = ~rd_or
    rd_xor = rs1 ^ rs2
    rd_add,c_add = n_adder_carry(rs1, rs2_to_add, add_or_sub)
    rd_mul,c_mul = mul(rs1, rs2)
    rd_div = div(rs1, rs2)

    rd = mux_n(alucode[0:3], (rd_and, rd_or, rd_nor, rd_xor, rd_add, rd_add, rd_mul, rd_div))


    flag_z = ~or_n_bits(rd)
    flag_n = rd[rd.bus_size-1]
    flag_c = mux(alucode[2], Constant("0"), mux_n(alucode[0:2], (c_add, ~c_add, c_mul, Constant("0"))))

    assert(rs1.bus_size == rs2.bus_size == rd.bus_size == rs2_to_add.bus_size)
    size = rs2.bus_size
    carry_v_add = (~rs1[size-1] & ~rs2_to_add[size-1] & rd[size-1]) | (rs1[size-1] & rs2_to_add[size-1] & ~rd[size-1])
    flag_v = mux(alucode[2], Constant("0"), mux(alucode[1], carry_v_add, Constant("0")))

    
    new_flags = (flag_z, flag_n, flag_c, flag_v )

    return (rd, new_flags)
