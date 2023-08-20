PYTHON         ?= python3
SHELL          := bash
.SHELLFLAGS    := -eu -o pipefail -c
.DEFAULT_GOAL   = all

.PHONY: all dev fmt fmtsql lint test

nox = $(VIRTUAL_ENV)/bin/nox
builtin_sql = src/textbox/storage/builtin/textbox.sql

all: $(nox)
	nox -s fmt lint test

dev: $(nox)

$(nox): pyproject.toml
	[[ -n $$VIRTUAL_ENV ]] || { echo CONTAIN ME; false; }
	$(PYTHON) -m pip install -e '.[dev]'
	touch $@

fmt lint test:: $(nox)
	$(nox) -s $@

fmt:: fmtsql

fmtsql:
	npx sql-formatter $(builtin_sql) --fix --config sql-formatter.json
