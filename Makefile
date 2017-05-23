export PYTHONPATH=.

all: test

test:
	py.test

lint:
	pylint --disable C,R *.py
