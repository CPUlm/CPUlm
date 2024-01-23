#!/bin/bash


sed -i -e '$a\    \pc.set_as_output("pc");r2.set_as_output("r2");r3.set_as_output("r3");r4.set_as_output("r4");r5.set_as_output("r5");r6.set_as_output("r6");r28.set_as_output("rout");r31.set_as_output("rpriv")  ### for the test ###' src/main.py


make
mkdir -p build
make -C ../CSimulator
make -C ../Assembler

../CSimulator/csimulator --disable-screen cpulm.net build
cd build/ && clang -g *.c && cd ..

red='\033[0;31m'
noColor='\033[0m'

for ulmFile in test/*.ulm; do
	echo $ulmFile
	echo -en "${red}"
	./../Assembler/asm $ulmFile
	echo -en "${red}"
    diff -w -B <(./build/a.out -p ${ulmFile/.ulm/.po} -d ${ulmFile/.ulm/.do}) ${ulmFile/.ulm/.out}
	echo -en "${noColor}"
done

sed -i '/### for the test ###/d' src/main.py 
rm -rf test/*.do
rm -rf test/*.po


