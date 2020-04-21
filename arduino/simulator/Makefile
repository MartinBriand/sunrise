SRC = $(wildcard *.c) $(wildcard *.cpp) $(wildcard *.ino)
HEAD = $(wildcard *.h) $(wildcard *.hpp)
# The working directory, where everything will be copied
DIR = .work
# The location of the libraries provided by the simulator
PACK = ../../simulator/pack
# IMPORTANT : Do not change this value ! It has to be shared with the Makefile in the simulator implementation
SIM = simulator.elf
.PHONY: clean

SIM: $(SRC) $(HEAD)
	# Removing the preexisting build dir if it exists
	rm -rf $(DIR)
	# Creatin the build directory
	mkdir $(DIR)
	# Copying the simulator implementation in the working dir
	cp $(PACK)/* $(DIR)
	# Copying arduino source to the working directory
	cp $(SRC) $(HEAD) $(DIR)
	# Compiling the arduino code with the Makefile provided by the simulator
	$(MAKE) -C $(DIR)
	# Copying the result to the current directory
	cp $(DIR)/$(SIM) ./
	#
	# ---> SUCCESS : Simulation has been compiled successfully <---
	#

clean:
	# Removing hidden working directory
	rm -rf $(DIR)
	# Deleting the build simulation
	rm -f $(SIM)
	# Deleting simulation output
	rm -f outfile.csv
