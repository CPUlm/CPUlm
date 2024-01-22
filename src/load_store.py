from constants import *
from tools import *


def load_store(instruction, regs_old):
    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    imm = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+2*REG_BITS+IMM_BITS]
    lhw = instruction[OPCODE_BITS+2*REG_BITS+IMM_BITS]
    rd = get_reg(id_rd, regs_old)
    rs = get_reg(id_rs, regs_old)

    ram_is_untouched = instruction[0]
    
    cst16 = Constant("0"*(WORD_SIZE - IMM_BITS))
    imm_dec = mux(lhw, cst16+imm, imm+cst16)
    rd_imm,_ = n_adder(imm_dec, rs)
    
    
    write_enable = instruction[1]
    rd_load = RAM(WORD_SIZE, WORD_SIZE, rs, write_enable, rd, rs)

    new_rd = mux(ram_is_untouched, mux(write_enable, rd_load, rd), rd_imm)
    regs_new = update_regs(regs_old, id_rd, new_rd)

    return (regs_new,)


