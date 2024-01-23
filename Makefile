SHELL := /bin/bash

cpulm.net: src/main.py src/constants.py src/alu.py src/load_store.py src/shift.py src/jmp.py src/tools.py
	@sed -i "s|carotte\.lib_carotte|lib_carotte|g" src/constants.py
	-python3 carotte/carotte.py src/main.py -o cpulm.net
	@sed -i "s|lib_carotte|carotte\.lib_carotte|g" src/constants.py

clean:
	-rm src/__pycache__ -r
	-rm carotte/__pycache__ -r
	-rm cpulm.net

test: cpulm.net
	./run_tests.sh

assembler:
	make -C ../Assembler

csimulator:
	make -C ../CSimulator

chrono: cpulm.net assembler csimulator
	@mkdir -p build
	@../Assembler/asm chrono.ulm
	@../CSimulator/csimulator --disable-screen cpulm.net build
	@cd build/ && clang -g *.c
	time build/a.out -p chrono.po -d chrono.do
	@rm -f chrono.do
	@rm -f chrono.po

.PHONY: all clean
