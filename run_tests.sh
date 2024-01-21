#!/bin/bash

<<<<<<< HEAD
=======
make all

>>>>>>> origin/main
make build file=../CPUlm/cpulm.net -C ../SimulateurC


red='\033[0;31m'
noColor='\033[0m'

<<<<<<< HEAD
for poFile in test/*.po; do
	echo $poFile
	echo -en "${red}"
    diff -w -B <(./../SimulateurC/build/a.out -p $poFile -d ${poFile/.po/.do}) ${poFile/.po/.out} 
	echo -en "${noColor}"
done
=======
for ulmFile in test/*.ulm; do
	echo $ulmFile
	echo -en "${red}"
	./../Assembler/asm $ulmFile
    diff -w -B <(./../SimulateurC/build/a.out -p ${ulmFile/.ulm/.po} -d ${ulmFile/.ulm/.do}) ${ulmFile/.ulm/.out} 
	echo -en "${noColor}"
done

rm -rf test/*.do
rm -rf test/*.po

>>>>>>> origin/main
