from constants import *
from tools import *

def alu(instruction, regs_old):
    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    
    rs1 = get_reg(id_rs1, regs_old)
    rs2 = get_reg(id_rs2, regs_old)

    rd,c = n_adder(rs1, rs2)

    regs_new = update_regs(regs_old, id_rd, rd)
    
    

    new_flags = (Constant("0"), Constant("0"), Constant("0"), Constant("0") )
    return (regs_old, new_flags)
