#!/bin/bash

make
make build file=../CPUlm/cpulm.net -C ../CSimulator


red='\033[0;31m'
noColor='\033[0m'

for ulmFile in test/*.ulm; do
	echo $ulmFile
	echo -en "${red}"
	./../Assembler/asm $ulmFile
	echo -en "${red}"
    diff -w -B <(./../CSimulator/build/a.out -p ${ulmFile/.ulm/.po} -d ${ulmFile/.ulm/.do}) ${ulmFile/.ulm/.out} 
	echo -en "${noColor}"
done

rm -rf test/*.do
rm -rf test/*.po
