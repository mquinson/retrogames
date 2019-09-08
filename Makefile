all: engine.tar.gz engine.zip

engine.tar.gz: engine/*.py engine/README
	tar cfz engine.tar.gz engine/*.py engine/README

engine.zip: engine/*.py engine/README
	zip engine engine/*.py engine/README
