#!/bin/bash

make build file=../CPUlm/cpulm.net -C ../SimulateurC


red='\033[0;31m'
noColor='\033[0m'

for poFile in test/*.po; do
	echo $poFile
	echo -en "${red}"
    diff -w -B <(./../SimulateurC/build/a.out -p $poFile -d ${poFile/.po/.do}) ${poFile/.po/.out} 
	echo -en "${noColor}"
done
