all: src/main.py
	@sed -i "s|carotte\.lib_carotte|lib_carotte|g" src/constants.py
	-python3 carotte/carotte.py src/main.py
	@sed -i "s|lib_carotte|carotte\.lib_carotte|g" src/constants.py

clean:
	-rm src/__pycache__ -r
	-rm carotte/__pycache__ -r

