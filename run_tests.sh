#!/bin/bash

make all

make build file=../CPUlm/cpulm.net -C ../SimulateurC


red='\033[0;31m'
noColor='\033[0m'

for ulmFile in test/*.ulm; do
	echo $ulmFile
	echo -en "${red}"
	./../Assembler/asm $ulmFile
    diff -w -B <(./../SimulateurC/build/a.out -p ${ulmFile/.ulm/.po} -d ${ulmFile/.ulm/.do}) ${ulmFile/.ulm/.out} 
	echo -en "${noColor}"
done

rm -rf test/*.do
rm -rf test/*.po

