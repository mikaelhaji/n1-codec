.PHONY: all clean python cpp

SHELL := /bin/bash

all: python

python: encode decode

cpp: encode_cpp decode_cpp

encode: encode.py
	ln -sf encode.py encode
	chmod +x encode

decode: decode.py
	ln -sf decode.py decode
	chmod +x decode

encode_cpp: encode.c
	gcc -O3 -o encode encode.c
	strip encode
	chmod +x encode

decode_cpp: decode.c
	gcc -O3 -o decode decode.c
	strip decode
	chmod +x decode


eval:
	sudo bash eval.sh	

grid:
	sudo bash grid_search.sh	


clean:
	rm -f encode decode
	

install:
	pip install -r requirements.txt
