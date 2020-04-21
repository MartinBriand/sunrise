# Prepares the pack folder with all the source required to make the simulator work correctly.
# In order to use the simulator, you can just put your arduino files in the same folder as everything contained in the pack folder and it will compile a simulation for you.

.PHONY: install clean

install:
	# Installing the core of the simulator
	$(MAKE) -C core install
	# Installing the arduino emulation
	$(MAKE) -C arduino install
	# Installing the SoftwareSerial emulation library
	$(MAKE) -C SoftwareSerial install
	# Installing the Kangaroo emulation library
	$(MAKE) -C Kangaroo install
	#
	# ---> SUCCESS : pack folder is ready <---
	#

clean:
	# Removing everything from the pack directory
	rm -f pack/*
