.PHONY: all install run debug clean lint lint-strict

PYTHON = python3
CONFIG = config.json

all: run

install:
	$(PYTHON) -m pip install pygame flake8 mypy mazegenerator-2.1.0-py3-none-any.whl

run: install
	$(PYTHON) game.py $(CONFIG)

debug:
	$(PYTHON) -m pdb game.py $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache *.pyc

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
