SRC = Kangaroo.cpp
HEAD = Kangaroo.h
# (Software) Serial Header
SRHEAD = SoftwareSerial.h
TEST = test.cpp
TOUT = test.elf
PACK = ../pack/

.PHONY: install

TOUT: $(SRC) $(HEAD) $(SRHEAD) $(TEST)
	clang++ $(SRC) $(TEST) -o $(TOUT)

install:
	# Copying Kangaroo emulator header file
	cp $(HEAD) $(PACK)
	# Copying Kangaroo emulator source file
	cp $(SRC) $(PACK)
	# Done copying the Kangaroo emulator files
