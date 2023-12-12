from constants import *

def alu(instruction, regs_old):
    new_flags = (Constant("0"), Constant("0"), Constant("0"), Constant("0") )
    return (regs_old, new_flags)
