PYTHON         ?= python3
SHELL          := bash
.SHELLFLAGS    := -eu -o pipefail -c
.DEFAULT_GOAL   = all

nox = $(VIRTUAL_ENV)/bin/nox

all: $(nox)
	nox -s fmt lint test

.PHONY: dev
dev: $(nox)

$(nox): pyproject.toml
	[[ -n $$VIRTUAL_ENV ]] || { echo CONTAIN ME; false; }
	$(PYTHON) -m pip install -e '.[dev]'
	touch $@

.PHONY: fmt lint test
fmt lint test: $(nox)
	$(nox) -s $@
