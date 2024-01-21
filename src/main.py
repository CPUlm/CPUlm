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


    # extraction de registres ...


    # calcul du resultat pour chaque instruction possible

    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    rs1 = get_reg(id_rs1, regs_old)
    rs2 = get_reg(id_rs2, regs_old)
    rd = get_reg(id_rd, regs_old)


    # chacune renvoie un n-uplet contenant les nouvelles valeur

    alu_set = alu(instruction, rs1, rs2)                     # renvoie (rd, flags)
    shift_set = shift(instruction, rs1, rs2)                 # renvoie (rd,)
    load_store_set = load_store(instruction, rd, rs1)        # renvoie (regs,)
    jmp_set = jmp(instruction, rd, flags_old, pc_old)  # renvoie (pc,)

    # calcul deplaces :
    rd_if_change = mux_alu_shift_load(opcode, alu_set[0], shift_set[0], load_store_set[0])
    regs_if_change = update_regs(regs_old, id_rd, rd_if_change)

    # selection du resultat grace a l'opcode et les resultats recus

    pc_if_incr,carry = incr(pc_old)
    pc = mux_jmp(opcode, pc_if_incr, jmp_set[0])

    flags = mux_alu(opcode, flags_old, alu_set[1])
    flag_z = flags[0]
    flag_n = flags[1]
    flag_c = flags[2]
    flag_v = flags[3]

    regs = mux_jmp(opcode, regs_if_change, regs_old)
    r2 = regs[0]
    r3 = regs[1]
    r4 = regs[2]
    r5 = regs[3]
    r6 = regs[4]
    r7 = regs[5]
    r8 = regs[6]
    r9 = regs[7]
    r10 = regs[8]
    r11 = regs[9]
    r12 = regs[10]
    r13 = regs[11]
    r14 = regs[12]
    r15 = regs[13]
    r16 = regs[14]
    r17 = regs[15]
    r18 = regs[16]
    r19 = regs[17]
    r20 = regs[18]
    r21 = regs[19]
    r22 = regs[20]
    r23 = regs[21]
    r24 = regs[22]
    r25 = regs[23]
    r26 = regs[24]
    r27 = regs[25]
    r28 = regs[26]
    r29 = regs[27]
    r30 = regs[28]
    r31 = regs[29]

    pc.set_as_output("pc")
    r2.set_as_output("r2")
    r3.set_as_output("r3")
    r4.set_as_output("r4")
    r5.set_as_output("r5")
    r6.set_as_output("r6")
    r28.set_as_output("rout")
    r31.set_as_output("rpriv")


