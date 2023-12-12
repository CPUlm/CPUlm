from constants import *
from tools import incr_reg

allow_ribbon_logic_operations(True)

OPCODE_BITS = 5
ALU_BITS = 5
REG_BITS = 5
WORD_SIZE = 32


def main():
    pc_copy = Reg(Defer(REG_BITS, lambda: pc))

    write_ram_enable_copy = Reg(Defer(1, lambda: write_ram_enable))
    write_ram_addr_copy = Reg(Defer(REG_BITS, lambda: write_ram_addr_copy))
    write_ram_value_copy = Reg(Defer(WORD_SIZE, lambda: write_ram_value_copy))

    instruction = RAM(REG_BITS, WORD_SIZE, pc_copy, write_ram_enable_copy, write_ram_addr_copy, write_ram_value_copy)

    # n'importe quoi pour tout declarer
    pc = incr_reg(Reg(Defer(REG_BITS, lambda: pc)))
    write_ram_enable = ~write_ram_enable_copy
    write_ram_addr = ~write_ram_addr_copy
    write_ram_value = ~write_ram_value_copy

    instruction.set_as_output("instruction")
