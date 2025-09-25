PYTHON?=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python

.PHONY: setup lint test run web bench clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]

lint:
	$(PY) -m pyflakes sudoku tests

test:
	$(PY) -m pytest

run:
	$(PY) -m sudoku.cli --file puzzles/easy.txt --format grid

web:
	FLASK_APP=sudoku.web $(PY) -m flask run --reload --port 5000

bench:
	$(PY) -m sudoku.cli --bench puzzles/hard.txt

clean:
	rm -rf $(VENV)
