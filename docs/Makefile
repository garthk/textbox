.PHONY: clean html

PYTHON       ?= python3
SPHINXOPTS   ?=
SPHINXBUILD  ?= $(PYTHON) -m sphinx.cmd.build
BUILDDIR     ?= _build

sphinxopts    = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

html:
	$(SPHINXBUILD) -n -b html $(sphinxopts) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

clean:
	-rm -rf $(BUILDDIR)/*
