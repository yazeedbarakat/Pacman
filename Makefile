.PHONY: all install run debug clean lint lint-strict

PYTHON = python3
CONFIG = config.json

all: run

install:
	$(PYTHON) -m pip install pygame

run:
	$(PYTHON) game.py $(CONFIG)

debug:
	$(PYTHON) -m pdb game.py $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache *.pyc

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
