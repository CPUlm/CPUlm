from constants import *
from tools import *

def jmp(instruction, regs_old, flags, pc_old):
    rd_addr = instruction[OPCODE_BITS: OPCODE_BITS+REG_BITS]
    imm = instruction[OPCODE_BITS: OPCODE_BITS+IMM_BITS]
    flagsMask1 = instruction[OPCODE_BITS + REG_BITS: OPCODE_BITS + REG_BITS + FLAGS_BITS]
    flagsMask2 = instruction[OPCODE_BITS + IMM_BITS: OPCODE_BITS + IMM_BITS + FLAGS_BITS]
    opcode = instruction[0: OPCODE_BITS]
    
    cas34 = opcode[3] & (opcode[0] | opcode[1])
    flagOk = test_flags(flags, Mux(cas34, flagsMask1, flagsMask2))
    
    rien = incr(pc_old)
    dest1 = get_reg(rd_addr, regs_old)
    dest2 = Mux(flagOk, rien, dest1)
    dest3,_ = n_adder(pc_old, imm+Constant("0"*(WORD_SIZE-IMM_BITS)))
    dest4 = Mux(flagOk, rien, dest3)

    dest = Mux(cas34, Mux(opcode[0], dest2, dest1), Mux(opcode[0], dest4, dest3))

    return (regs_old, dest)
