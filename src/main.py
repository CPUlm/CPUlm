from constants import *
from tools import *
from alu import *
from shift import *
from load_store import *
from jmp import *

allow_ribbon_logic_operations(True)


def main():
    pc_old = Reg(Defer(5, lambda: pc))

    regs_old =   ( Reg(Defer(REG_BITS, lambda: r2)),
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
    # chacune renvoie un n-uplet contenant les nouvelles valeur

    alu_set = alu(instruction, regs_old)                     # renvoie (regs, flags)
    shift_set = shift(instruction, regs_old)                 # renvoie (regs) sous forme de 1-uplet
    load_store_set = load_store(instruction, regs_old)             # renvoie (regs)
    jmp_set = jmp(instruction, regs_old, flags_old, pc_old)  # renvoie (regs, pc)

    # selection du resultat grace a l'opcode et les resultats recus

    r2 = regs_old[0]
    r3 = regs_old[1]
    r4 = regs_old[2]
    r5 = regs_old[3]
    flag_z = flags_old[0]
    flag_n = flags_old[1]
    flag_c = flags_old[2]
    flag_v = flags_old[3]
    pc = incr(pc_old)

    instruction.set_as_output("instruction")
