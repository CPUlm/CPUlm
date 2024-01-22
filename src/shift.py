from constants import *
from tools import *
from math import *


def shift(instruction, rs1, rs2):
    n = rs1.bus_size
    rs2 = rs2[0:5]

    # Logical Shift Left:
    lsl_lst = [rs1]
    for i in range(1,n):
        z_i = Constant("0"*i)
        lsl_lst.append( z_i + rs1[0:n-i] )
    lsl = mux_n(rs2, lsl_lst)

    # Logical Shift Right
    lsr_lst = [rs1]
    for i in range(1,n):
        z_i = Constant("0"*i)
        lsr_lst.append( rs1[i:n] + z_i )
    lsr = mux_n(rs2, lsr_lst)


    # Arithmetic Shift Right :
    asr1_lst = [rs1]            # dans le cas ou le bit de poids fort est 1
    for i in range(1,n):
        o_i = Constant("1"*i)
        asr1_lst.append( rs1[i:n] + o_i )
    asr1 = mux_n(rs2, asr1_lst)
    asr = mux(rs1[n-1],lsr,asr1)
    
    # mux :
    rd = mux(instruction[0], asr, mux(instruction[1], lsl, lsr))
    
    return (rd,)
