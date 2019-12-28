.PHONY: default \
	virtualenv \
	dev-tools

default: virtualenv

virtualenv: bin/activate
	. bin/activate ; \
	pip install -r requirements.txt

dev-tools: bin/activate
	. bin/activate; \
	pip install -r dev-tools-requirements.txt

bin/activate:
	virtualenv -p python3.7 .

clean:
	git clean -xdf
