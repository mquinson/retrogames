# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = RetroGames
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile intl

intl:
	for lang in fr ; do \
	  rm -rf intl; \
	  $(SPHINXBUILD) -M html "$(SOURCEDIR)" intl $(SPHINXOPTS) -D language="$$lang" $(O); \
	  for f in intl/html/*.html ; do \
	    file=`basename $$f`; \
	    echo $$file; \
	    cp $$f build/html/$$file.$$lang; \
	  done; \
	done
	rm -rf intl;

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)