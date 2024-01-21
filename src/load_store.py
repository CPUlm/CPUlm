from constants import *
from tools import *


def load_store(instruction, rd, rs):
    imm = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+2*REG_BITS+IMM_BITS]
    lhw = instruction[OPCODE_BITS+2*REG_BITS+IMM_BITS]

    ram_is_untouched = instruction[0]
    
    cst16 = Constant("0"*(WORD_SIZE - IMM_BITS))
    imm_dec = mux(lhw, cst16+imm, imm+cst16)
    rd_imm,_ = n_adder(imm_dec, rs)
    
    
    write_enable = instruction[1]
    rd_load = RAM(WORD_SIZE, WORD_SIZE, rs, write_enable, rd, rs)

    new_rd = mux(ram_is_untouched, mux(write_enable, rd_load, rd), rd_imm)

    return (new_rd,)


