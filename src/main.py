from constants import *
from tools import *

allow_ribbon_logic_operations(True)


def main():
    pc_old = Reg(Defer(5, lambda: pc))

    write_ram_enable_copy = Reg(Defer(1, lambda: write_ram_enable))
    write_ram_addr_copy = Reg(Defer(REG_BITS, lambda: write_ram_addr_copy))
    write_ram_value_copy = Reg(Defer(WORD_SIZE, lambda: write_ram_value_copy))

    instruction = RAM(REG_BITS, WORD_SIZE, pc_old, write_ram_enable_copy, write_ram_addr_copy, write_ram_value_copy)

    # n'importe quoi pour tout declarer
    pc = incr(pc_old)
	 
    write_ram_enable = ~write_ram_enable_copy
    write_ram_addr = ~write_ram_addr_copy
    write_ram_value = ~write_ram_value_copy

    instruction.set_as_output("instruction")
