from lib_carotte import *
allow_ribbon_logic_operations(True)



def main():
    rs1 = Input(32)
    rs2 = Input(32)

    rd_and = rs1 & rs2

    rd_and.set_as_output("rd_and")
