from constants import *
from tools import *

def alu(instruction, regs_old):
    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    alucode = instruction[OPCODE_BITS + 3*REG_BITS : OPCODE_BITS + 3*REG_BITS + ALU_BITS]
    
    rs1 = get_reg(id_rs1, regs_old)
    rs2 = get_reg(id_rs2, regs_old)

    rd_and = rs1 & rs2
    rd_or = rs1 | rs2
    rd_nor = ~rd_or
    rd_xor = rs1 ^ rs2
    rd_add,_ = n_adder(rs1, rs2)
    rd_sub = rd_add                 # TODO
    rd_mul = rd_add                 # TODO
    rd_div = rd_add                 # TODO

    rd = mux_tuple(alucode[2], mux_tuple(alucode[1], mux_tuple(alucode[0], rd_and, rd_or),
                                                     mux_tuple(alucode[0], rd_nor, rd_xor)),
                               mux_tuple(alucode[1], mux_tuple(alucode[0], rd_add, rd_sub),
                                                     mux_tuple(alucode[0], rd_mul, rd_div)))


    regs_new = update_regs(regs_old, id_rd, rd_add)
    
    

    # TODO : gestion des flags
    new_flags = (Constant("0"), Constant("0"), Constant("0"), Constant("0") )

    return (regs_old, new_flags)
