from constants import *
from tools import *

allow_ribbon_logic_operations(True)


def main():
    pc_old = Reg(Defer(5, lambda: pc))

    reg_old =   ( Reg(Defer(REG_BITS, lambda: r2)),
                  Reg(Defer(REG_BITS, lambda: r3)),
                  Reg(Defer(REG_BITS, lambda: r4)),
                  Reg(Defer(REG_BITS, lambda: r5)) )
	
    flags_old = ( Reg(Defer(REG_BITS, lambda: flag_z)),
                  Reg(Defer(REG_BITS, lambda: flag_n)),
                  Reg(Defer(REG_BITS, lambda: flag_c)),
                  Reg(Defer(REG_BITS, lambda: flag_v)) )
	 

    instruction = ROM(REG_BITS, WORD_SIZE, pc_old)
    opcode = instruction[0 : OPCODE_BITS]

    # calcul du resultat pour chaque instruction possible
    # chacune renvoie un n-uplet contenant les nouvelles valeur de :
    # (pc, regs, ram_actions, flags )

    """
    alu_set = alu(instruction, ........)
    shift_set = shift(instruction,.....)
    load_store_set = load(instruction,....)
    jmp_set = jmp(instruction,....)
    """

    # selection du resultat grace a l'opcode et les resultats recus

    r2 = reg_old[0]
    r3 = reg_old[1]
    r4 = reg_old[2]
    r5 = reg_old[3]
    flag_z = flags_old[0]
    flag_n = flags_old[1]
    flag_c = flags_old[2]
    flag_v = flags_old[3]
    pc = incr(pc_old)

    instruction.set_as_output("instruction")
