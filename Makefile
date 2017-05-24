all: test lint

test:
	py.test tests/

lint:
	pylint --disable C,R *.py
