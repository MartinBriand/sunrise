# This Makefile compiles an arduino project with every other C and C++ source available in the current working directory into a simulation called simulation.elf

# IMPORTANT : Don't change this value, as it is hardcoded in other related Makefiles
SIM = simulator.elf
SRC = $(wildcard *.c) $(wildcard *.cpp) $(wildcard *.ino)
HEAD = $(wildcard *.h) $(wildcard *.hpp)

.PHONY: clean

SIM: $(SRC) $(HEAD)
	# Compiling the project
	c++ -x c++ $(SRC) -o $(SIM)

clean:
	# Deleting the compiled simulation
	rm -f $(SIM)
