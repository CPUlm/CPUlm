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
    pc_if_incr = incr(pc_old)

    # chacune renvoie un n-uplet contenant les nouvelles valeur

    alu_set = alu(instruction, rs1, rs2)                     # renvoie (rd, flags)
    shift_set = shift(instruction, rs1, rs2)                 # renvoie (rd,)
    load_store_set = load_store(instruction, rd, rs1)        # renvoie (regs,)
    jmp_set = jmp(instruction, rd, flags_old, pc_old, pc_if_incr)  # renvoie (pc,)

    # calcul deplaces :
    rd_if_change = mux_alu_shift_load(opcode, alu_set[0], shift_set[0], load_store_set[0])
    new_rd = mux_jmp(opcode, rd_if_change, rd)
    ##regs_if_change = update_regs(regs_old, id_rd, rd_if_change)

    rd_one_hot = one_hot(id_rd)

    # selection du resultat grace a l'opcode et les resultats recus

    pc = mux_jmp(opcode, pc_if_incr, jmp_set[0])

    flags = mux_alu(opcode, flags_old, alu_set[1])
    flag_z = flags[0]
    flag_n = flags[1]
    flag_c = flags[2]
    flag_v = flags[3]

    #regs = mux_jmp(opcode, regs_if_change, regs_old)
    r2 = mux(rd_one_hot[2], regs_old[0], new_rd)
    r3 = mux(rd_one_hot[3], regs_old[1], new_rd)
    r4 = mux(rd_one_hot[4], regs_old[2], new_rd)
    r5 = mux(rd_one_hot[5], regs_old[3], new_rd)
    r6 = mux(rd_one_hot[6], regs_old[4], new_rd)
    r7 = mux(rd_one_hot[7], regs_old[5], new_rd)
    r8 = mux(rd_one_hot[8], regs_old[6], new_rd)
    r9 = mux(rd_one_hot[9], regs_old[7], new_rd)
    r10 = mux(rd_one_hot[10], regs_old[8], new_rd)
    r11 = mux(rd_one_hot[11], regs_old[9], new_rd)
    r12 = mux(rd_one_hot[12], regs_old[10], new_rd)
    r13 = mux(rd_one_hot[13], regs_old[11], new_rd)
    r14 = mux(rd_one_hot[14], regs_old[12], new_rd)
    r15 = mux(rd_one_hot[15], regs_old[13], new_rd)
    r16 = mux(rd_one_hot[16], regs_old[14], new_rd)
    r17 = mux(rd_one_hot[17], regs_old[15], new_rd)
    r18 = mux(rd_one_hot[18], regs_old[16], new_rd)
    r19 = mux(rd_one_hot[19], regs_old[17], new_rd)
    r20 = mux(rd_one_hot[20], regs_old[18], new_rd)
    r21 = mux(rd_one_hot[21], regs_old[19], new_rd)
    r22 = mux(rd_one_hot[22], regs_old[20], new_rd)
    r23 = mux(rd_one_hot[23], regs_old[21], new_rd)
    r24 = mux(rd_one_hot[24], regs_old[22], new_rd)
    r25 = mux(rd_one_hot[25], regs_old[23], new_rd)
    r26 = mux(rd_one_hot[26], regs_old[24], new_rd)
    r27 = mux(rd_one_hot[27], regs_old[25], new_rd)
    r28 = mux(rd_one_hot[28], regs_old[26], new_rd)
    r29 = mux(rd_one_hot[29], regs_old[27], new_rd)
    r30 = mux(rd_one_hot[30], regs_old[28], new_rd)
    r31 = mux(rd_one_hot[31], regs_old[29], new_rd)

    pc.set_as_output("pc")
    r2.set_as_output("r2")
    r3.set_as_output("r3")
    r4.set_as_output("r4")
    r5.set_as_output("r5")
    r6.set_as_output("r6")
    r28.set_as_output("rout")
    r31.set_as_output("rpriv")
