VENV = venv
PYTHON = $(VENV)/bin/python3.9
PIP = $(VENV)/bin/pip
NAME = pypoca
.PHONY = help setup test run clean
.DEFAULT_GOAL = help

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	@python3.9 -m venv $(VENV)
	@$(PIP) install -U pip
	@$(PIP) install -r requirements-dev.txt

.PHONY: install
install: $(VENV)/bin/activate

.PHONY: version
version: $(VENV)/bin/activate
	@$(PYTHON) --version
	@$(PIP) --version
	@$(PIP) freeze

.PHONY: run
run: $(VENV)/bin/activate
	@$(PYTHON) -m ${NAME}

.PHONY: clean
clean:
	@$(PYTHON) -Bc "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"
	@$(PYTHON) -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: uninstall
uninstall:
	@rm -rf $(VENV)
