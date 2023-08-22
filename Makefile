PYTHON         ?= python3
SHELL          := bash
.SHELLFLAGS    := -eu -o pipefail -c
.DEFAULT_GOAL   = all

.PHONY: all clean dev docs fmt fmtsql lint test

nox = $(VIRTUAL_ENV)/bin/nox
builtin_sql = src/textbox/storage/builtin/textbox.sql

all: $(nox)
	nox -s fmt lint test docs

dev: $(nox)

docs:
	$(MAKE) -C docs html

$(nox): pyproject.toml
	[[ -n $$VIRTUAL_ENV ]] || { echo CONTAIN ME; false; }
	$(PYTHON) -m pip install -e '.[dev]'
	touch $@

fmt lint test:: $(nox)
	$(nox) -s $@

fmt:: fmtsql

fmtsql:
	npx sql-formatter $(builtin_sql) --fix --config sql-formatter.json

clean:
	rm -rf build src/textbox.egg-info
	$(MAKE) -C docs clean
