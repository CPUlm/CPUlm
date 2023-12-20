from constants import *
from tools import *
from alu import *
from shift import *
from load_store import *
from jmp import *

allow_ribbon_logic_operations(True)


def main():
    pc_old = Reg(Defer(WORD_SIZE, lambda: pc))

    regs_old =  ( Reg(Defer(WORD_SIZE, lambda: r2)),
                  Reg(Defer(WORD_SIZE, lambda: r3)),
                  Reg(Defer(WORD_SIZE, lambda: r4)),
                  Reg(Defer(WORD_SIZE, lambda: r5)),
                  Reg(Defer(WORD_SIZE, lambda: r6)),
                  Reg(Defer(WORD_SIZE, lambda: r7)),
                  Reg(Defer(WORD_SIZE, lambda: r8)),
                  Reg(Defer(WORD_SIZE, lambda: r9)),
                  Reg(Defer(WORD_SIZE, lambda: r10)),
                  Reg(Defer(WORD_SIZE, lambda: r11)),
                  Reg(Defer(WORD_SIZE, lambda: r12)),
                  Reg(Defer(WORD_SIZE, lambda: r13)),
                  Reg(Defer(WORD_SIZE, lambda: r14)),
                  Reg(Defer(WORD_SIZE, lambda: r15)),
                  Reg(Defer(WORD_SIZE, lambda: r16)),
                  Reg(Defer(WORD_SIZE, lambda: r17)),
                  Reg(Defer(WORD_SIZE, lambda: r18)),
                  Reg(Defer(WORD_SIZE, lambda: r19)),
                  Reg(Defer(WORD_SIZE, lambda: r20)),
                  Reg(Defer(WORD_SIZE, lambda: r21)),
                  Reg(Defer(WORD_SIZE, lambda: r22)),
                  Reg(Defer(WORD_SIZE, lambda: r23)),
                  Reg(Defer(WORD_SIZE, lambda: r24)),
                  Reg(Defer(WORD_SIZE, lambda: r25)),
                  Reg(Defer(WORD_SIZE, lambda: r26)),
                  Reg(Defer(WORD_SIZE, lambda: r27)),
                  Reg(Defer(WORD_SIZE, lambda: r28)),
                  Reg(Defer(WORD_SIZE, lambda: r29)),
                  Reg(Defer(WORD_SIZE, lambda: r30)),
                  Reg(Defer(WORD_SIZE, lambda: r31)))

    flags_old = ( Reg(Defer(1, lambda: flag_z)),
                  Reg(Defer(1, lambda: flag_n)),
                  Reg(Defer(1, lambda: flag_c)),
                  Reg(Defer(1, lambda: flag_v)))
 

    instruction = ROM(WORD_SIZE, WORD_SIZE, pc_old)
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

    regs = mux_opcode(opcode, alu_set[0], shift_set[0], load_store_set[0], jmp_set[0])
    r2 = regs[0]
    r3 = regs[1]
    r4 = regs[2]
    r5 = regs[3]
    r6 = regs[3]
    r7 = regs[3]
    r8 = regs[3]
    r9 = regs[3]
    r10 = regs[3]
    r11 = regs[3]
    r12 = regs[3]
    r13 = regs[3]
    r14 = regs[3]
    r15 = regs[3]
    r16 = regs[3]
    r17 = regs[3]
    r18 = regs[3]
    r19 = regs[3]
    r20 = regs[3]
    r21 = regs[3]
    r22 = regs[3]
    r23 = regs[3]
    r24 = regs[3]
    r25 = regs[3]
    r26 = regs[3]
    r27 = regs[3]
    r28 = regs[3]
    r29 = regs[3]
    r30 = regs[3]
    r31 = regs[3]

