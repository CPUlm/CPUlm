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

chrono:
	./../Assembler/asm chrono.ulm
	make build file=../CPUlm/cpulm.net -C ../SimulateurC
	time ./../SimulateurC/build/a.out -p chrono.po -d chrono.do > tmp
	rm -f chrono.do
	rm -f chrono.po
	cat tmp

a:
	time grep "aa" cpulm.net

.PHONY: all clean
