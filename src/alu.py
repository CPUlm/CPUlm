from constants import *
from tools import *

def big_adder(lst):
    # retourne la somme de tous les elements de lst
    n = len(lst)
    assert(n > 0)
    if n == 1:
        return lst[0]
    else:
        m = n//2
        s1 = big_adder(lst[0:m])
        s2 = big_adder(lst[m:n])
        s,c = n_adder(s1, s2)
        return s

def mul(a, b):
    assert(a.bus_size == b.bus_size)
    n = a.bus_size
    zn = Constant("0"*n)

    result = zn
    for i in range(n):
        ajout = mux(a[i], zn, b)
        result,_ = n_adder(result, ajout)
        b = b[1:n] + Constant("0")
        
    return result

def or_n_bits(a):
    r = a[0]
    for i in range(1, a.bus_size):
        r = r | a[i]
    return r

def div(dividende, diviseur):
    # TODO reflechir a la division signee
    assert(dividende.bus_size == diviseur.bus_size)
    n = dividende.bus_size

    dividende_rogne = dividende[n-1]
    trop_court = or_n_bits(diviseur[1:n])   # les seuls nombre restants possible sont 0 (on ignore) et 1 (on suppose donc qu'on divise par 1)
    plus_grand = (~trop_court) & dividende_rogne
    quotient = plus_grand
    dividende_rogne = mux(plus_grand, dividende_rogne, Constant("0"))

    for i in range(1,n):
        assert (dividende_rogne.bus_size == i)
        
        dividende_rogne = dividende_rogne + dividende[n-i-1]
        trop_court = or_n_bits(diviseur[i+1:n]) if i+1 != n else Constant("0")
        diff,_ = n_adder(dividende_rogne, incr(~diviseur[0:i+1]))

        plus_grand = (~trop_court) & diff[diff.bus_size-1]

        quotient = quotient + plus_grand
        dividende_rogne = mux(plus_grand, dividende_rogne, diff)
    return quotient


        
        

        
    return dividende_rogne

def alu(instruction, regs_old):
    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    alucode = instruction[OPCODE_BITS + 3*REG_BITS : OPCODE_BITS + 3*REG_BITS + ALU_BITS]
    
    rs1 = get_reg(id_rs1, regs_old)
    rs2 = get_reg(id_rs2, regs_old)
    rs2_neg = incr(~rs2)

    rd_and = rs1 & rs2
    rd_or = rs1 | rs2
    rd_nor = ~rd_or
    rd_xor = rs1 ^ rs2
    rd_add,_ = n_adder(rs1, rs2)
    rd_sub,_ = n_adder(rs1, rs2_neg)
    rd_mul = mul(rs1, rs2) if WITH_MUL else rs1
    rd_div = div(rs1, rs2) if WITH_DIV else rs1

    rd = mux_n(alucode[0:3], (rd_and, rd_or, rd_nor, rd_xor, rd_add, rd_sub, rd_mul, rd_div))


    regs_new = update_regs(regs_old, id_rd, rd_add)
    
    

    # TODO : gestion des flags
    new_flags = (Constant("0"), Constant("0"), Constant("0"), Constant("0") )

    return (regs_old, new_flags)
