from constants import *
from tools import *

def jmp(instruction, dest_jmp, flags, pc_old):
    imm = instruction[OPCODE_BITS: OPCODE_BITS+IMM24_BITS]
    flags_mask1 = instruction[OPCODE_BITS + REG_BITS: OPCODE_BITS + REG_BITS + FLAGS_BITS]
    flags_mask2 = instruction[OPCODE_BITS + IMM24_BITS : OPCODE_BITS + IMM24_BITS + FLAGS_BITS]
    opcode = instruction[0: OPCODE_BITS]
    
    has_imm = opcode[3] & (opcode[0] | opcode[1])
    flag_ok = test_flags(flags, mux(has_imm, flags_mask1, flags_mask2))
    
    incr_pc,_ = incr(pc_old)
    dest_jmpc = mux(flag_ok, incr_pc, dest_jmp)
    
    complet_signe = mux(imm[WORD_SIZE-OPCODE_BITS-FLAGS_BITS-1], Constant("0"*(WORD_SIZE-IMM24_BITS)), Constant("1"*(WORD_SIZE-IMM24_BITS)))
    dest_jmpi,_ = n_adder(pc_old, imm+complet_signe)
    dest_jmpic = mux(flag_ok, incr_pc, dest_jmpi)

    dest = mux(has_imm, mux(opcode[0], dest_jmpc, dest_jmp), mux(opcode[0], dest_jmpic, dest_jmpi))

    return (dest,)
