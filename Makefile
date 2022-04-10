#!/usr/bin/python3

INPUTDIR=./tests/*.txt

all:
	cp src/main.py parcial-relaxada
	chmod 744 parcial-relaxada

run:
	clear; for i in $(INPUTDIR); do echo "./parcial-relaxada < $$i"; ./parcial-relaxada < $$i; done;

clean:
	rm parcial-relaxada
