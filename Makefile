
# Minimal Makefile for Sphinx documentation

# The build directory
BUILDDIR   = _build

# The source directory
SRCDIR     = source

# The output directory
OUTPUTDIR  = $(BUILDDIR)/html

# Sphinx build command
SPHINXBUILD = sphinx-build
SPHINXOPTS   = -q

# Use the sphinx-build command to build the docs
.PHONY: help html

# Default target: build the HTML docs
html:
	$(SPHINXBUILD) -b html $(SRCDIR) $(OUTPUTDIR)

# Help target: show usage of make commands
help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  html   Build the HTML documentation"
