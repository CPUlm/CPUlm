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
    load_store_set = load_store(instruction, regs_old)       # renvoie (regs)
    jmp_set = jmp(instruction, regs_old, flags_old, pc_old)  # renvoie (regs, pc)

    # selection du resultat grace a l'opcode et les resultats recus

    pc_if_incr = incr(pc_old)
    pc = mux_jmp(opcode, pc_if_incr, jmp_set[1])

    flags = mux_alu(opcode, flags_old, alu_set[1])
    flag_z = flags[0]
    flag_n = flags[1]
    flag_c = flags[2]
    flag_v = flags[3]

    regs = select_opcode(opcode, alu_set[0], shift_set[0], load_store_set[0], jmp_set[0])
    r2 = regs[0]
    r3 = regs[1]
    r4 = regs[2]
    r5 = regs[3]

