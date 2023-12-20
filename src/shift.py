from constants import *
from tools import *


def shift(instruction, regs_old):
    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    
    rs1 = get_reg(id_rs1, regs_old)
    rs2 = get_reg(id_rs2, regs_old)[0:5]

    # left :
    # TODO
    lsl = mux5bits(rs2,
        rs1,
        rs1[1:32] + Constant("0"),
        rs1[2:32] + Constant("0"*2),
        rs1[3:32] + Constant("0"*3),
        rs1[4:32] + Constant("0"*4),
        rs1[5:32] + Constant("0"*5),
        rs1[6:32] + Constant("0"*6),
        rs1[7:32] + Constant("0"*7),
        rs1[8:32] + Constant("0"*8),
        rs1[9:32] + Constant("0"*9),
        rs1[10:32] + Constant("0"*10),
        rs1[11:32] + Constant("0"*11),
        rs1[12:32] + Constant("0"*12),
        rs1[13:32] + Constant("0"*13),
        rs1[14:32] + Constant("0"*14),
        rs1[15:32] + Constant("0"*15),
        rs1[16:32] + Constant("0"*16),
        rs1[17:32] + Constant("0"*17),
        rs1[18:32] + Constant("0"*18),
        rs1[19:32] + Constant("0"*19),
        rs1[20:32] + Constant("0"*20),
        rs1[21:32] + Constant("0"*21),
        rs1[22:32] + Constant("0"*22),
        rs1[23:32] + Constant("0"*23),
        rs1[24:32] + Constant("0"*24),
        rs1[25:32] + Constant("0"*25),
        rs1[26:32] + Constant("0"*26),
        rs1[27:32] + Constant("0"*27),
        rs1[28:32] + Constant("0"*28),
        rs1[29:32] + Constant("0"*29),
        rs1[30:32] + Constant("0"*30),
        rs1[31:32] + Constant("0"*31))
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
