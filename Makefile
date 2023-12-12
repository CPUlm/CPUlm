all: main.py
	./carotte.py/carotte.py main.py

clean:
	rm __pycache__ -r
	rm carotte.py/__pycache__ -r

