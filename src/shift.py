from constants import *
from tools import *


def shift(instruction, regs_old):
    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    
    rs1 = get_reg(id_rs1, regs_old)
    rs2 = get_reg(id_rs2, regs_old) & Constant("0"*(WORD_SIZE-5) + "1"*5)

    # left :
    # TODO
    lsl = rs1
    lslRegs = update_regs(regs_old, id_rd, lsl)

    #right :
    # TODO
    asr = rs1
    asrRegs = update_regs(regs_old, id_rd, asr)

    lsr = rs1
    lsrRegs = update_regs(regs_old, id_rd, lsr)

    # mux :
    regs_new = mux_tuple(instruction[0], asrRegs, mux_tuple(instruction[1], lslRegs, lsrRegs))

    return (regs_new,)
