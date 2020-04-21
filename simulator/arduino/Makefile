SRC = arduino.cpp Serial.cpp
HEAD = arduino.hpp
TEST = test.cpp
TOUT = test.elf
# The pack directory location
DIR = ../pack/
.PHONY: install

TOUT: $(SRC) $(HEAD) $(TEST)
	clang++ $(SRC) $(TEST) -o $(TOUT)

install:
	# Copying arduino emulation header files
	cp $(HEAD) $(DIR)
	# Copying arduino emulation source files
	cp $(SRC) $(DIR)
	# Done installing arduino emulation files
