# My alpha trimmer makefile

.PHONY: all
all:
	./trim.sh
	
.PHONY: install_tools
install_tools:
	./install.sh

