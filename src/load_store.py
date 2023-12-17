from constants import *
from tools import *

def load_store(instruction, regs_old):
    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    imm = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+2*REG_BITS+IMM_BITS]
    lhw = instruction[OPCODE_BITS+2*REG_BITS+IMM_BITS]
    rd = get_reg(id_rd, regs_old)
    rs = get_reg(id_rs, regs_old)

    doNotUseRam = instruction[0]
    
    cst16 = Constant("0"*(WORD_SIZE - IMM_BITS))
    immDec = Mux(lhw, imm+cst16, cst16+imm)
    rd_imm,_ = n_adder(immDec, rs)
    
    
    writeEnable = instruction[1]
    rd_load = RAM(WORD_SIZE, WORD_SIZE, rs, writeEnable, rd, rs)

    new_rd = Mux(doNotUseRam, Mux(writeEnable, rd_load, rd), rd_imm)
    regs_new = update_regs(regs_old, id_rd, new_rd)
    return (regs_new,)


