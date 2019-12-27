.PHONY: default\
	virtualenv

default: virtualenv

virtualenv: bin/activate

bin/activate:
	virtualenv -p python3.7 .
