from constants import *
from tools import *
from math import *


def shift(instruction, regs_old):

    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    
    rs1 = get_reg(id_rs1, regs_old)
    n = rs1.bus_size
    m = round(log2(n))
    rs2 = get_reg(id_rs2, regs_old)[0:m]


    # Logical Shift Left:
    lsl_lst = [rs1]
    for i in range(1,n):
        z_i = Constant("0"*i)
        lsl_lst.append( z_i + rs1[0:n-i] )
    lsl = mux_n(rs2, lsl_lst)
    lsl_regs = update_regs(regs_old, id_rd, lsl)

    # Logical Shift Right
    lsr_lst = [rs1]
    for i in range(1,n):
        z_i = Constant("0"*i)
        lsr_lst.append( rs1[i:n] + z_i )
    lsr = mux_n(rs2, lsr_lst)
    lsr_regs = update_regs(regs_old, id_rd, lsr)


    # Arithmetic Shift Right :
    asr1_lst = [rs1]            # dans le cas ou le bit de poids fort est 1
    for i in range(1,n):
        o_i = Constant("1"*i)
        asr1_lst.append( rs1[i:n] + o_i )
    asr1 = mux_n(rs2, asr1_lst)
    asr_regs = update_regs(regs_old, id_rd, mux(rs1[n-1],lsr,asr1))
    
    # mux :
    regs_new = mux(instruction[0], asr_regs, mux(instruction[1], lsl_regs, lsr_regs))
    
    return (regs_new,)
