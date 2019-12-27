.PHONY: default \
	virtualenv

default: virtualenv

virtualenv: bin/activate
	. bin/activate ; \
	pip install -r requirements.txt

bin/activate:
	virtualenv -p python3.7 .

clean:
	git clean -xdf
