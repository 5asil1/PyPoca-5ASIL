VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
NAME = pypoca
.PHONY = help setup test run clean
.DEFAULT_GOAL = help

.PHONY: help
help:				## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install: $(VENV)/bin/activate	## Install the virtual env project in dev mode.

.PHONY: version
version: $(VENV)/bin/activate	## Show the current environment.
	@echo "Running using $(VENV)"
	$(PYTHON) --version
	$(PIP) --version

.PHONY: format
format: $(VENV)/bin/activate	## Format code using black & isort.
	isort ${NAME}/
	brunette ${NAME}/ --config=setup.cfg

.PHONY: lint
lint: $(VENV)/bin/activate	## Format code using black & isort.
	flake8 ${NAME}/ --config=setup.cfg --count --show-source --statistics --benchmark
	brunette ${NAME}/ --config=setup.cfg --check
	interrogate ${NAME}/ --config=setup.cfg
	vulture ${NAME}/ --ignore-names on_* --min-confidence 80
	mypy ${NAME}/ --ignore-missing-imports

.PHONY: run
run: $(VENV)/bin/activate
	$(PYTHON) -m ${NAME}

.PHONY: test
test: $(VENV)/bin/activate	## Run tests and generate coverage report.
	pytest -v --cov=${NAME}/ --cov-report=xml -l --tb=short --maxfail=1

.PHONY: watch
watch: $(VENV)/bin/activate	## Run tests on every change.
	ls **/**.py | entr pytest -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: clean
clean:				## Clean unused files.
	@find ${NAME} -name '*.pyc' -exec rm -f {} \;
	@find ${NAME} -name '__pycache__' -exec rm -rf {} \;
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
uninstall:			## Uninstall the virtual env project.
	@rm -rf $(VENV)

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	python3 -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -r requirements-dev.txt
