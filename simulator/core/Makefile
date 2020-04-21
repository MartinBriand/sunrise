SRC = main.cpp Constants.cpp
HEAD = export.hpp
# The name of the pack Makefile before it gets copied
MK_FUTURE = Makefile.future
# The name of the pack Makefile once copied
MK = Makefile
PACK = ../pack/

.PHONY: install

install:
	# Copying emulator core header file
	cp $(HEAD) $(PACK)
	# Copying emulator core source file
	cp $(SRC) $(PACK)
	# Copying emulator Makefile
	cp $(MK_FUTURE) $(PACK)/$(MK)
	# Done copying emulator core files
