from constants import *
from tools import *


def shift(instruction, regs_old):

    # définition de constantes (permet d'éviter quelles soient définies plusieurs fois dans la netlist)
    z1 = Constant("0")
    z2 = Constant("0"*2)
    z3 = Constant("0"*3)
    z4 = Constant("0"*4)
    z5 = Constant("0"*5)
    z6 = Constant("0"*6)
    z7 = Constant("0"*7)
    z8 = Constant("0"*8)
    z9 = Constant("0"*9)
    z10 = Constant("0"*10)
    z11 = Constant("0"*11)
    z12 = Constant("0"*12)
    z13 = Constant("0"*13)
    z14 = Constant("0"*14)
    z15 = Constant("0"*15)
    z16 = Constant("0"*16)
    z17 = Constant("0"*17)
    z18 = Constant("0"*18)
    z19 = Constant("0"*19)
    z20 = Constant("0"*20)
    z21 = Constant("0"*21)
    z22 = Constant("0"*22)
    z23 = Constant("0"*23)
    z24 = Constant("0"*24)
    z25 = Constant("0"*25)
    z26 = Constant("0"*26)
    z27 = Constant("0"*27)
    z28 = Constant("0"*28)
    z29 = Constant("0"*29)
    z30 = Constant("0"*30)
    z31 = Constant("0"*31)
    o1 = Constant("1")
    o2 = Constant("1"*2)
    o3 = Constant("1"*3)
    o4 = Constant("1"*4)
    o5 = Constant("1"*5)
    o6 = Constant("1"*6)
    o7 = Constant("1"*7)
    o8 = Constant("1"*8)
    o9 = Constant("1"*9)
    o10 = Constant("1"*10)
    o11 = Constant("1"*11)
    o12 = Constant("1"*12)
    o13 = Constant("1"*13)
    o14 = Constant("1"*14)
    o15 = Constant("1"*15)
    o16 = Constant("1"*16)
    o17 = Constant("1"*17)
    o18 = Constant("1"*18)
    o19 = Constant("1"*19)
    o20 = Constant("1"*20)
    o21 = Constant("1"*21)
    o22 = Constant("1"*22)
    o23 = Constant("1"*23)
    o24 = Constant("1"*24)
    o25 = Constant("1"*25)
    o26 = Constant("1"*26)
    o27 = Constant("1"*27)
    o28 = Constant("1"*28)
    o29 = Constant("1"*29)
    o30 = Constant("1"*30)
    o31 = Constant("1"*31)





    id_rd = instruction[OPCODE_BITS : OPCODE_BITS+REG_BITS]
    id_rs1 = instruction[OPCODE_BITS+REG_BITS : OPCODE_BITS+2*REG_BITS]
    id_rs2 = instruction[OPCODE_BITS+2*REG_BITS : OPCODE_BITS+3*REG_BITS]
    
    rs1 = get_reg(id_rs1, regs_old)
    rs2 = get_reg(id_rs2, regs_old)[0:5]

    # Logical Shift Right:
    lsl = mux5bits(rs2,(
        rs1,
        rs1[1:32] + z1,
        rs1[2:32] + z2,
        rs1[3:32] + z3,
        rs1[4:32] + z4,
        rs1[5:32] + z5,
        rs1[6:32] + z6,
        rs1[7:32] + z7,
        rs1[8:32] + z8,
        rs1[9:32] + z9,
        rs1[10:32] + z10,
        rs1[11:32] + z11,
        rs1[12:32] + z12,
        rs1[13:32] + z13,
        rs1[14:32] + z14,
        rs1[15:32] + z15,
        rs1[16:32] + z16,
        rs1[17:32] + z17,
        rs1[18:32] + z18,
        rs1[19:32] + z19,
        rs1[20:32] + z20,
        rs1[21:32] + z21,
        rs1[22:32] + z22,
        rs1[23:32] + z23,
        rs1[24:32] + z24,
        rs1[25:32] + z25,
        rs1[26:32] + z26,
        rs1[27:32] + z27,
        rs1[28:32] + z28,
        rs1[29:32] + z29,
        rs1[30:32] + z30,
        rs1[31:32] + z31))
    lsl_regs = update_regs(regs_old, id_rd, lsl)

    # Logical Shift Right
    lsr = mux5bits(rs2,(
        rs1,
        z1 + rs1[0:31],
        z2 + rs1[0:30],
        z3 + rs1[0:29],
        z4 + rs1[0:28],
        z5 + rs1[0:27],
        z6 + rs1[0:26],
        z7 + rs1[0:25],
        z8 + rs1[0:24],
        z9 + rs1[0:23],
        z10 + rs1[0:22],
        z11 + rs1[0:21],
        z12 + rs1[0:20],
        z13 + rs1[0:19],
        z14 + rs1[0:18],
        z15 + rs1[0:17],
        z16 + rs1[0:16],
        z17 + rs1[0:15],
        z18 + rs1[0:14],
        z19 + rs1[0:13],
        z20 + rs1[0:12],
        z21 + rs1[0:11],
        z22 + rs1[0:10],
        z23 + rs1[0:9],
        z24 + rs1[0:8],
        z25 + rs1[0:7],
        z26 + rs1[0:6],
        z27 + rs1[0:5],
        z28 + rs1[0:4],
        z29 + rs1[0:3],
        z30 + rs1[0:2],
        z31 + rs1[0:1]))
    lsr_regs = update_regs(regs_old, id_rd, lsr)


    # Arithmetic Shift Right :
    asr1 = mux5bits(rs2,(            # dans le cas ou le bit de poids fort est 1
        rs1,
        o1 + rs1[0:31],
        o2 + rs1[0:30],
        o3 + rs1[0:29],
        o4 + rs1[0:28],
        o5 + rs1[0:27],
        o6 + rs1[0:26],
        o7 + rs1[0:25],
        o8 + rs1[0:24],
        o9 + rs1[0:23],
        o10 + rs1[0:22],
        o11 + rs1[0:21],
        o12 + rs1[0:20],
        o13 + rs1[0:19],
        o14 + rs1[0:18],
        o15 + rs1[0:17],
        o16 + rs1[0:16],
        o17 + rs1[0:15],
        o18 + rs1[0:14],
        o19 + rs1[0:13],
        o20 + rs1[0:12],
        o21 + rs1[0:11],
        o22 + rs1[0:10],
        o23 + rs1[0:9],
        o24 + rs1[0:8],
        o25 + rs1[0:7],
        o26 + rs1[0:6],
        o27 + rs1[0:5],
        o28 + rs1[0:4],
        o29 + rs1[0:3],
        o30 + rs1[0:2],
        o31 + rs1[0:1]))
    asr_regs = update_regs(regs_old, id_rd, mux_tuple(rs1[WORD_SIZE-1],lsr,asr1))
    
    # mux :
    regs_new = mux_tuple(instruction[0], asr_regs, mux_tuple(instruction[1], lsl_regs, lsr_regs))
    
    return (regs_new,)
