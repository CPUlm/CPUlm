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
    rd_mul = mul(rs1, rs2)
    rd_div = rd_add                 # TODO

    rd = mux_n(alucode[0:3], (rd_and, rd_or, rd_nor, rd_xor, rd_add, rd_sub, rd_mul, rd_div))


    regs_new = update_regs(regs_old, id_rd, rd_add)
    
    

    # TODO : gestion des flags
    new_flags = (Constant("0"), Constant("0"), Constant("0"), Constant("0") )

    return (regs_old, new_flags)
