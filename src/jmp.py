from constants import *
from tools import *

def jmp(instruction, regs_old, flags, pc_old):
    rd_addr = instruction[OPCODE_BITS: OPCODE_BITS+REG_BITS]
    imm = instruction[OPCODE_BITS: OPCODE_BITS+IMM24_BITS]
    flags_mask1 = instruction[OPCODE_BITS + REG_BITS: OPCODE_BITS + REG_BITS + FLAGS_BITS]
    flags_mask2 = instruction[OPCODE_BITS + IMM24_BITS : OPCODE_BITS + IMM24_BITS + FLAGS_BITS]
    opcode = instruction[0: OPCODE_BITS]
    
    has_imm = opcode[3] & (opcode[0] | opcode[1])
    flag_ok = test_flags(flags, Mux(has_imm, flags_mask1, flags_mask2))
    
    incr_pc = incr(pc_old)
    dest_jmp = get_reg(rd_addr, regs_old)
    dest_jmpc = Mux(flag_ok, incr_pc, dest_jmp)
    
    complet_signe = mux(imm[WORD_SIZE-OPCODE_BITS-FLAGS_BITS-1], Constant("0"*(WORD_SIZE-IMM24_BITS)), Constant("1"*(WORD_SIZE-IMM24_BITS)))
    dest_jmpi,_ = n_adder(pc_old, imm+complet_signe)
    dest_jmpic = Mux(flag_ok, incr_pc, dest_jmpi)

    dest = Mux(has_imm, Mux(opcode[0], dest_jmpc, dest_jmp), Mux(opcode[0], dest_jmpic, dest_jmpi))

    return (regs_old, dest)
