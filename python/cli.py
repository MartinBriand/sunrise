# bonjour
import os
import sys
import pickle  # pickle is in stdlib so we won't ever get an import error here.
import argparse  # same, argparse is part of stdlib
from textwrap import fill  # same, part of stdlib
try:
    import numpy as np
except ImportError:
    print("---X This tools requires the numpy module, which seems currently unavailable. Please install numpy before tying to use this tool. The recommended syntax to install numpy is :\n$ python3 -m pip install numpy")
    sys.exit(1)
try:
    import cable_robot as cr  # Our module to command the robot.
except ImportError:
    print("---X This command line tool is an interface to a python module (more like script actually) called cable_robot. In order to use this tool you must first make sure that this module is available (it currently isn't). The recommended way to do this is to grab the source code cable_robot.py and put it in the same directory as this cli.py file. The source code for cable_robot is available freely on GitHub at [...].")
    sys.exit(1)


class CLI(object):
    """docstring for CLI."""

    def __init__(self, cli_args):
        # List of all parameters accepted to trigger auto mode.
        self.auto_list = ["auto", "AUTO", "Auto", "a", "A"]
        # Same for manual mode.
        self.manual_list = ["manual", "MANUAL", "Manual", "m", "M"]
        # Same for time step.
        self.time_list = ["time", "TIME", "Time", "t", "T"]
        # Same for frequency (for users mor comfortable working with that).
        self.freq_list = ["frequency", "FREQUENCY", "Frequency", "freq", "FREQ", "Freq", "f", "F"]
        # Same for help.
        self.help_list = ["help", "HELP", "Help", "h", "H", "?"]
        # To leave the tool.
        self.exit_list = ["exit", "EXIT", "Exit", "e", "E", "leave", "LEAVE", "Leave", "l", "L", "quit", "QUIT", "Quit", "q", "Q"]
        self.halt_list = ["halt", "HALT", "Halt", "h", "H", "stop", "STOP", "Stop", "s", "S"]
        self.time_step = 0.1
        # Full output by default.
        self.silence = 2 - cli_args.verbosity
        # Safe mode, annoys users for their safety
        self.safe = not cli_args.unsafe
        self.speed_limit = 100  # steps per second, above that value the robot is deemed unstable.

    def read_command(self, command):
        # cursor is used to keep track of how many argument we read from the users command.
        cursor = 0
        split_command = str.split(command)
        if len(split_command) == 0:
            # Empty line, we can just ignore it
            return
        # else ...
        instruction = split_command[0]
        cursor += 1
        if instruction in self.auto_list:
            return self.process_auto(split_command, cursor)
        elif instruction in self.manual_list:
            return self.process_manual()
        elif instruction in self.time_list:
            return self.process_time(split_command, cursor)
        elif instruction in self.freq_list:
            return self.process_freq(split_command, cursor)
        elif instruction in self.help_list:
            return self.process_help(split_command, cursor)
        elif instruction in self.exit_list:
            return self.exit()
        elif instruction in self.halt_list:
            cr.halt()
            self.bprint("Halting the robot ...")
            return
        else:
            self.bprint(f"The inputed command {command} could not be parsed, because the tool did not understand the term '{instruction}'. If you wish to you can use :\n'>> help'\nThat instruction will bring a list of the available instruction and their use cases.", 2)
            return

    def exit(self):
        # Used to leave the tool. When triggered this will always halt the robot.
        cr.halt()
        self.bprint("Leaving the tool... The robot is being halted.")
        sys.exit(0)

    def process_freq(self, split_command, cursor):
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            self.bprint(f"At what pace do you want the robot to move ? That pace can be computed from the step frequency value, which is the amount of steps the robot will perform during a single second. The current value of the step frequency is {int(1/self.time_step)}.", 1)
            self.bprint(f"The syntax to change the step frequency is :\n'>> frequency <step frequency>'\nStep frequency has to be a positive int value and should be reasonably small. In safe mode the programm will refuse arbitrary large values, because the behavior of the robot is undefined at a fast pace.")
            return
        else:
            freq = split_command[cursor]
            cursor += 1
            try:
                int_freq = int(freq)
                if int_freq <= 0:
                    self.bprint(f"You asked the robot to take {freq} step each second, but negative (zero included) values are not valid in that context. Please input a positive integer instead.", 2)
                    return
                elif int_freq > self.speed_limit:
                    if self.safe:
                        self.bprint(f"Caution, the behavior of the robot is strongly undefined at a high speed. The inputed speed is too high to be accepted when the robot is in safe mode. Please input a step frequency that is smaller than {self.speed_limit} seconds (i.e. {1/self.speed_limit} seconds between each steps). If you know what you are doing you can also try to raise the speed limit, please consult the help manual to see how to do that.\nThe inputed step frequency {int_freq} has been refused, it will remain at its old value {int(1/self.time_step)}", 2)
                    else:
                        self.bprint(f"The inputed speed is above the preset speed limit (of {self.speed_limit} steps per second). However the robot currently is in unsafe mode, hence the value {int_freq} steps per second won't be refused. Please be carefull during your manipulations.", 1)
                        self.time_step = 1/int_freq
                else:
                    self.time_step = 1/int_freq

            except ValueError as e:
                self.bprint(f"The value of the step frequency has to be a positive int, but the tool could not parse {freq} as an int. The correct syntax to set the step frequency is :\n'>> frequency <step frequency>'", 2)
                return

    def process_time(self, split_command, cursor):
        if len(split_command) == cursor:
            # i.e. we have no more arguments available
            self.bprint(f"At what pace do you want the robot to move ? That pace is computed from the time step value, which is the amount of time the robot will take to perform an infinitesimal step. The current value of the time step is {self.time_step}.", 1)
            self.bprint(f"The syntax to change the time step is :\n'>> time <time step>'\nTime step has to be a float value and should be reasonably small. In safe mode the programm will refuse arbitrary large values, because the behavior of the robot is undefined at a fast pace.")
            return
        else:
            pace = split_command[cursor]
            cursor += 1
            try:
                float_pace = float(pace)
                if float_pace <= 0:
                    self.bprint(f"You asked the robot to take a step each {pace} seconds, but negative (zero included) values are not valid in that context. Please input a positive float instead.", 2)
                    return
                elif float_pace * self.speed_limit < 1:
                    if self.safe:
                        self.bprint(f"Caution, the behavior of the robot is strongly undefined at a high speed. The inputed speed is too high to be accepted when the robot is in safe mode. Please input a time step that is bigger than {1/self.speed_limit} seconds (i.e. {self.speed_limit} steps per seconds). If you know what you are doing you can also try to raise the speed limit, please consult the help manual to see how to do that.\nThe inputed time step {float_pace} has been refused, it will remain at its old value {self.time_step}", 2)
                    else:
                        self.bprint(f"The inputed speed is above the preset speed limit (of {self.speed_limit} steps per second). However the robot currently is in unsafe mode, hence the value {float_pace} seconds (i.e. {int(1/float_pace)} steps per second) won't be refused. Please be carefull during your manipulations.", 1)
                        self.time_step = float_pace
                else:
                    self.time_step = float_pace

            except ValueError as e:
                self.bprint(f"The value of the time step has to be a positive float, but the tool could not parse {pace} as a float. The correct syntax to set the time step is :\n'>> time <time step>'", 2)
                return

    def process_auto(self, split_command, cursor):
        file_path = ""
        if len(split_command) == cursor:
            # i.e. no other argument, we will look if we find any suiting file.
            self.bprint("You didn't supply file for the trajectory. Looking for an appropriate file ...", 1)
            try:
                file_path = self.lookup_trajectory_file()
            except FileNotFoundError as e:
                self.bprint("The tool was unable to find any suitable file for the trajectory. Please supply a trajectory in order to use the auto mode.", 2)
                self.bprint("The minimal syntax to supply a trajectory is :\n'>> auto <trajectory_file>'")
                return
        else:
            file_path = split_command[cursor]
            cursor += 1
            if not os.path.exists(file_path):
                self.bprint(f"The supplied file {file_path} does not exists", 2)
                return

        # We have found the trajectory file, we now need to find how to read it.
        method = ""
        if len(split_command) == cursor:
            # i.e. no other argument, we have to guess how to read the file. Our guess will of course rely on the file's extension.
            self.bprint("Guessing how to read the file ...")
            file_name, extension = os.path.splitext(file_path)

            if extension == ".npy":
                self.bprint("Your file seems to be a saved numpy array.")
                method = "npy"
            elif extension == ".txt":
                self.bprint("Your file seems to be a numpy array saved as text.")
                method = "txt"
            elif extension == ".dat":
                self.bprint("Your file seems to be a numpy array saved in a plateform dependant way.")
                method = "dat"
            elif extension == "":
                self.bprint("Your file seems to be a pickled numpy array")
                method = "pickle"
            elif extension == ".csv":
                self.bprint("Your file seems to be numpy array saved in the csv format")
                method = "csv"
        else:
            method = split_command[cursor]
            known_methods = ["npy", "txt", "dat", "csv", "pickle"]
            if method not in known_methods:
                self.bprint(f"The reading method you specified : {method} is unknown to this tool. Please use one of npy, txt, dat, csv or pickle. Read the help manual in order to see how to use either of these.", 2)
                return

        array = np.array(0)
        if method == "npy":
            try:
                array = np.load(file_path)
            except IOException as e:
                self.bprint(f"The data in the file {file_path} could not be loaded. Consider explicitely telling the tool how to open your file, or using another format if the problem persists.", 2)
                self.bprint(f"The minimal syntax to explain how to open a file is :\n'>> auto <trajectory_file> <method>'\n Method should be one of 'pickle', 'npy', 'dat', 'csv', 'txt'. Read the help for more information about those methods.")
                return
        elif method == "txt":
            try:
                array = np.loadtxt(file_path, dtype=float)
            except Exception as e:
                # I don't know which exception to expect here, but hopefully nothing will go wrong here
                self.bprint(f"The data in the file {file_path} could not be loaded. Consider explicitely telling the tool how to open your file, or using another format if the problem persists.", 2)
                self.bprint(f"The minimal syntax to explain how to open a file is :\n'>> auto <trajectory_file> <method>'\n Method should be one of 'pickle', 'npy', 'dat', 'csv', 'txt'. Read the help for more information about those methods.")
                return
        elif method == "dat":
            try:
                # The dat format saves array in one line (like its machine representation) so we must to reshape it.
                array_flat = np.fromfile(file_path, dtype=float)
                size = np.size(array_flat)
                array = array_flat.reshape((size//6, 6))
                self.bprint("The dat file format is deprecated and dangerous as it is not plateform independant. Please use the npy format as an alternative instead.", 1)
            except Exception as e:
                # same
                self.bprint(f"The data in the file {file_path} could not be loaded. Consider explicitely telling the tool how to open your file, or using another format if the problem persists.", 2)
                self.bprint(f"The minimal syntax to explain how to open a file is :\n'>> auto <trajectory_file> <method>'\n Method should be one of 'pickle', 'npy', 'dat', 'csv', 'txt'. Read the help for more information about those methods.")
                return
        elif method == "csv":
            try:
                array = np.loadtxt(file_path, dtype=float, delimiter=',')
            except Exception as e:
                # Well, I guess I could get used to this. But really, the numpy documentation never seems to mention the raised exceptions
                self.bprint(f"The data in the file {file_path} could not be loaded. Consider explicitely telling the tool how to open your file, or using another format if the problem persists.", 2)
                self.bprint(f"The minimal syntax to explain how to open a file is :\n'>> auto <trajectory_file> <method>'\n Method should be one of 'pickle', 'npy', 'dat', 'csv', 'txt'. Read the help for more information about those methods.")
                return
        else:   # i.e. method = pickle
            try:
                with open(file_path, 'rb') as source_file:
                    array = pickle.load(source_file)
                self.bprint("The pickle module is designed to serialize almost any object python can produce and is not specific to numpy. As such, it is not very efficient as saving / loading numpy arrays and should be avoided. Please use npy instead", 1)
            except pickle.UnpicklingError as e:
                self.bprint(f"The data in the file {file_path} could not be loaded. Consider explicitely telling the tool how to open your file, or using another format if the problem persists.", 2)
                self.bprint(f"The minimal syntax to explain how to open a file is :\n'>> auto <trajectory_file> <method>'\n Method should be one of 'pickle', 'npy', 'dat', 'csv', 'txt'. Read the help for more information about those methods.")
                return

        # We finally start the trajectory computation
        cr.auto(array, self.time_step)
        return

    def process_manual(self):
        vector = np.zeros(8)
        # Used in unsafe mode
        old_vector = np.zeros(8)
        keep_manual = True
        halt_list = self.halt_list
        exit_list = self.exit_list
        self.bprint("Manual command mode triggered.\nIn this mode you can only control a single motor at once. The syntax to use manual mode is :\n'(manual) >> <motor number>'\nThis will cause the targeted motor (numbered from 1 to 8) to start moving at the desired pace while all other motors will stay still. You can use that syntax again to move the focus to another motor. If you wish unroll the cables of that motor instead you can use :\n'(manual) >> -<motor number>'\nThat will cause the motor to start moving in reverse.\nIf you for some reason wish to halt the robot you can use :\n'(manual) >> halt'\nIn order to leave manual mode just use :\n'(manual) >> exit'")
        while keep_manual:
            # Note that we will block on the following line until something is entered.
            command = input("(manual) >> ")
            vector = np.zeros(8)
            if command in halt_list or command in exit_list:
                # leaving the manual mode of courses halts the robot.
                # Note that the robot would be halted regardless at the end of the loop, but just to be sure we use the halt command.
                cr.halt()
                if command in exit_list:
                    keep_manual = False
                    self.bprint("Leaving manual mode ...")
                    # We leave the loop
                    break
                else:
                    # If we had just halted we start listening to user input again
                    continue
            elif command.startswith("help"):
                split_command = command.split()
                self.process_help(split_command, 1)
                if self.safe:
                    self.bprint("Displaying help in manual mode halts the robot", 1)
                else:
                    # We just assume that the user wants the robot to keep moving because we are running in unsafe mode.
                    vector = old_vector
            else:
                try:
                    motor = int(command)
                    if motor in range(1, 9):
                        vector[motor - 1] = 1
                    elif motor in [-i for i in range(1, 9)]:
                        vector[-(1 + motor)] = -1
                    else:
                        self.bprint(f"The input {command} could not be interpreted correctly. You have to input something that is either an int between 1 and 8 (included) in order to have one of the motors move, or an integer between -8 and -1 in order to command the motors to move backwards, or a command to halt or exit the manual mode (namely 'halt' and 'exit').", 2)
                        if self.safe:
                            self.bprint(f"The robot is being halted because of the bad input.", 1)
                        else:
                            self.bprint(f"The robot is running in unsafe mode, hence we are assuming that you want to keep the movment going. If you in fact wish to halt the robot please input 'halt'", 1)
                            vector = old_vector
                except ValueError as e:
                    self.bprint(f"The input {command} could not be interpreted correctly. You have to input something that is either an int between 1 and 8 (included) in order to have one of the motors move, or an integer between -8 and -1 in order to command the motors to move backwards, or a command to halt or exit the manual mode (namely 'halt' and 'exit').", 2)
                    if self.safe:
                        self.bprint(f"The robot is being halted because of the bad input.", 1)
                    else:
                        self.bprint(f"The robot is running in unsafe mode, hence we are assuming that you want to keep the movment going. If you in fact wish to halt the robot please input 'halt'", 1)
                        vector = old_vector
            # Sending the instruction to the robot.
            cr.manual(vector, self.time_step)
            old_vector = vector
        return

    # That one needs to be a method in order to have access to the bprint method, which in turn needs to be a method in order to have access to the self.silent value.
    def lookup_trajectory_file(self):
        def lookup(file_path):
            self.bprint(f"Looking up {file_path} ...")
            if os.path.exists(file_path):
                self.bprint(f"File {file_path} found.")
                return True
            # else ...
            return False

        lookup_basename_list = ["trajectoire", "TRAJECTOIRE", "Trajectoire", "trajectory", "TRAJECTORY", "Trajectory", "traj", "TRAJ", "Traj"]
        lookup_extension_list = [".txt", ".csv", ".npy", ".dat", ""]

        for basename in lookup_basename_list:
            for extension in lookup_extension_list:
                file_found = lookup(f"{basename}{extension}")
                if file_found:
                    # Returning path of the found file
                    return f"{basename}{extension}"

        # Caught by read_command, we haven't found any suitable file
        raise FileNotFoundError()

    def bprint(self, msg, mode=0):
        # mode 0 means information, 1 means warning and 2 means error
        wrapped_msg_list = []
        for line in iter(msg.splitlines()):
            wrapped_msg_list.append(fill(line, width=80))
        wrapped_msg = "\n".join(wrapped_msg_list)
        if mode >= self.silence:
            if mode == 1:
                print(f"---! {wrapped_msg}")
                return
            elif mode == 2:
                print(f"---X {wrapped_msg}")
                return
            else:   # i.e. mode == 0
                print(f"---> {wrapped_msg}")
                return
        # else ... be silent of course.

    def process_help(self, split_command, cursor):
        if len(split_command) == cursor:
            # i.e. no more arguments to read, just printing command list.
            command_help = (
            "All possible input commands are :\n\n"
            " - auto : triggers auto mode. In that mode the robot will follow a predefined trajectory. For more informations about auto mode, please use :\n'>> help auto'\n\n"
            " - manual : triggers manual mode. In that mode you are able to control each of the robot's motors individually. For more informations about manual mode, please use :\n'>> help manual'\n\n"
            " - time : Changes the speed of the robot by specifying the time it will have to perform each individual step. For more informations about the time command, please use :\n'>> help time'\n\n"
            " - frequency : Changes the speed of the robot by specifying how often it will perform a step. For more informations about the time command, please use :\n'>> help frequency'\n\n"
            " - help : Brings out various help message, including this one.\n\n"
            " - halt : Will stop the robot immediately, regardless of what it was doing.\n\n"
            " - exit : Leaves this tool. If your are using a keyboard you can also use EOF shortcut (Ctrl + D on Linux for instance). This will also cause the robot to halt.\n"
            )
            self.bprint(command_help)
            return
        else:
            topic = split_command[cursor]
            cursor += 1
            if topic in self.exit_list:
                self.bprint("The exit command will exit the tool. This will always cause the robot to halt.")
                return
            elif topic in self.halt_list:
                self.bprint("The halt command will force the robot to stop immediately. This instruction works in every mode and can be used even if the robot is moving in auto mode.")
                return
            elif topic in self.help_list:
                self.bprint("Is the robot not working so badly that you started writing random input in the tool ? If so, have you tried (in that order) :\n\n - Checking that everything is correctly plugged-in ?\n - Turning it off and on again ?\n - Looking for help online ?\n - Yelling at the machine ?\n\nIf you are unsure where the problem stems from, try initializing the robot in manual mode. That should help you check whether the communication is working properly.\nIf you are able to initialize the robot in manual mode but can't use it in auto mode, then try reading the detailed help about the various ways to give the targeted trajectory to the robot using :\n'>> help auto'\nIf none of that works then you may (or may not) have some hardware issue. Please read the online manual to get an idea of how to troubleshoot that.")
                return
            elif topic in self.time_list:
                time_help = (
                "The time command is used to alter the pace of the robot by specifying how much time each of its steps should last. That time is specified in seconds as a positive float.\n"
                f"Please pay attention to the fact that the behavior of the robot at a high speed is undefined and that it could become dangerous if pushed too far beyond its limit. Because of that, this tool will refuse any time step value that would be below {1/self.speed_limit} seconds. If you know what you are doing you can also change that limit.\n"
                "The syntax to use the command time is :\n"
                "'>> time <time step>'\n"
                f"Where <time step> is a positive float bigger than the current limit of {1/self.speed_limit} seconds.\n"
                f"The current time step of the robot is {self.time_step} seconds.\n"
                "Note that specifying the pace using time or frequency is strictly equivalent."
                )
                self.bprint(time_help)
                return
            elif topic in self.freq_list:
                freq_help = (
                "The time command is used to alter the pace of the robot by specifying how much steps it should perform each seconds. That frequency is specified in steps per seconds as a positive integer.\n"
                f"Please pay attention to the fact that the behavior of the robot at a high speed is undefined and that it could become dangerous if pushed too far beyond its limit. Because of that, this tool will refuse any step frequency value that would be above {self.speed_limit} steps per seconds. If you know what you are doing you can also change that limit.\n"
                "The syntax to use the command time is :\n"
                "'>> frequency <step frequency>'\n"
                f"Where <step frequency> is a positive integer smaller than the current limit of {self.speed_limit} steps per seconds.\n"
                f"The current step frequency of the robot is {int(1/self.time_step)} steps per second.\n"
                "Note that specifying the pace using time or frequency is strictly equivalent."
                )
                self.bprint(freq_help)
                return
            elif topic in self.manual_list:
                manual_help = (
                "The manual command is used to trigger the manual mode. In manual mode you can control each of the motors individually, and you can use this to roll or unroll any of the cables. That is especially usefull when you have to initialize the robot before using it. The syntax to trigger manual mode is :\n"
                "'>> manual'\n"
                "Once in manual mode most commands are not longer available (namely auto, time and frequency). The help command is still available in manual mode. The manual mode is an interactive one, because the motors will move in real time as you tell them to.\n"
                "The 8 motors of the robot are labeled from 1 to 8. In order to command the ith motor to start rolling its cable, just use :\n"
                "'(manual) >> i'\n"
                f"That will cause the ith motor to ... well ... start rolling its cable at the pace specified beforehand (using the time or frequency command). That pace currently is {self.time_step} seconds per steps or {int(1/self.time_step)} steps per second.\n"
                "If you instead need to unroll the ith cable, the syntax is :\n"
                "'(manual) >> -i'\n"
                "At any moment, if you wish to halt the robot you can just input :\n"
                "'(manual) >> halt'\n"
                "If you wish to leave the manual mode (note that you will remain in the tool, and the commands auto, time and frequency will become available again), just input :\n"
                "'(manual) >> exit'\n"
                "Leaving the manual mode will of course halt the robot."
                )
                self.bprint(manual_help)
                return
            elif topic in self.auto_list:
                if len(split_command) == cursor:
                    # No more arguments, the user just wants informations on the auto mode.
                    auto_help = (
                    "The auto command is used to trigger the automatic mode. In auto mode the robot will try to follow a given trajectory. You don't have to (and can't) control the motors individually in auto mode.\n\n"
                    "The complete syntax of the auto command is :\n"
                    "'>> auto <trajectory file> <reading method>'\n"
                    "Where trajectory file is the file in which the tool will read the trajectory and reading method is the method that should be used to get the numpy array of the trajectory from the file. Both arguments are optionnal.\n\n"
                    "Trajectory file is a path to the file and can be either relative to your working directory or absolute. The trajctory file must contain (in some form) a numpy array of the trajectory and nothing else. That numpy array must have 6 columns (3 positions and 3 rotations) but can have as many rows as you want it to.\n"
                    "Reading method has to be one of npy (recommended), txt, csv, dat (deprecated), pickle. For mor information on either of those methods just use :\n"
                    "'>> help auto <method>'\n\n"
                    "If no files are provided, the tool will try to guess which file in the current working directory you want it to use. It will look for files whose name resembles 'trajectory' and whose extension is one of .npy, .txt, .csv, .dat or no extension at all. The tool will use the first matching file it finds.\n\n"
                    "If no reading method is provided, the tool will try to guess the appropriate one using the extension of the file. A file that ends with .npy will be read using the npy method, a file in .txt with the txt method, a file in .csv with the csv method, a file in .dat with the dat method and a file without extension with the pickle method."
                    )
                    self.bprint(auto_help)
                    return
                else:
                    method = split_command[cursor]
                    cursor += 1
                    if method == "npy":
                        npy_help = (
                        "The npy method is the prefered way to save numpy array for this tool. Given that the numpy array you want to save is called trajectory and the file you want to save it to is trajectory.npy, the code snippet to save the array is:\n\n{\n"
                        "# import numpy as np\n"
                        "np.save('trajectory.npy', trajectory)\n}\n\n"
                        "And that's it. Pretty convenient is it not ? The file will be read by this tool using the snippet :\n\n{\n"
                        "# import numpy as np\n"
                        "array = np.load('trajectory.py')\n}\n\n"
                        "Remember that your array must have 6 columns (3 positions + 3 rotations) but can have as many rows as you'd like."
                        )
                        self.bprint(npy_help)
                        return
                    elif method == "txt":
                        txt_help = (
                        "The txt method is not one I would recommend, but at least it saves the arrays in a human readable way, which you might be interested in. Given that the numpy array you want to save is called trajectory and the file you want to save it to is trajectory.txt, the code snippet to save the array is:\n\n{\n"
                        "# import numpy as np\n"
                        "np.savetxt('trajectory.txt', trajectory)\n}\n\n"
                        "The array can then be read using any application you'd like (for instance notepad on Windows) if you wish to verify it, but be aware that the csv method might be a better fit for that use case. The file will be read by this tool using the snippet :\n\n{\n"
                        "# import numpy as np\n"
                        "array = np.loadtxt('trajectory.txt', dtype=float)\n}\n\n"
                        "Remember that your array must have 6 columns (3 positions + 3 rotations) but can have as many rows as you'd like."
                        )
                        self.bprint(txt_help)
                        return
                    elif method == "csv":
                        csv_help = (
                        "The csv file format ('comma separated values') is a well established one and is supported so that you may be able to use this tool more easily with other solutions that may not support anything else. Given that the numpy array you want to save is called trajectory and the file you want to save it to is trajectory.csv, the code snippet to save the array is:\n\n{\n"
                        "# import numpy as np\n"
                        "np.savetxt('trajectory.csv', trajectory, delimiter=',')\n}\n\n"
                        "csv files can be opened by most bureautic applications such as LibreOffice or Excel for verification. The file will be read by this tool using the snippet :\n\n{\n"
                        "# import numpy as np\n"
                        "array = np.loadtxt('trajectory.csv', dtype=float, delimiter=',')\n}\n\n"
                        "Remember that your array must have 6 columns (3 positions + 3 rotations) but can have as many rows as you'd like."
                        )
                        self.bprint(csv_help)
                        return
                    elif method == "dat":
                        dat_help = (
                        "The dat file format is a performance oriented numpy array saving method that gives up on cross-plateform compatibility for enhanced performances. However this tool isn't performance oriented (by a long shot) so using the dat method here is more likely to create bugs than it is to be of any help. If you need good performances for some reason please use the .npy format which is also very efficient. Given that the numpy array you want to save is called trajectory and the file you want to save it to is trajectory.dat, the code snippet to save the array is:\n\n{\n"
                        "# import numpy as np\n"
                        "trajectory.tofile('trajectory.dat')\n}\n\n"
                        "Once again, those .dat files aren't plateform independant, so you if you created them on another machine you are likely to run into issues here. The file will be read by this tool using the snippet :\n\n{\n"
                        "# import numpy as np\n"
                        "array = np.fromfile('trajectory.dat', dtype=float)\n}\n\n"
                        "Remember that your array must have 6 columns (3 positions + 3 rotations) but can have as many rows as you'd like."
                        )
                        self.bprint(dat_help)
                        return
                    elif method == "pickle":
                        pickle_help = (
                        "The pickle tool is useed to serialize any python object. It is not specific to numpy and to be fair not a great choice for numpy array serialization. Please use the npy method instead. Given that the numpy array you want to save is called trajectory and the file you want to save it to is also called trajectory, the code snippet to save the array is:\n\n{\n"
                        "# import pickle\n"
                        "with open('trajectory', 'wb') as pickle_file:\n"
                        "    pickle.dump(trajectory, pickle_file)\n}\n\n"
                        "The main asset of pickle is that it can be used on almost any python object, but once again for numpy array they aren't especially handy. The file will be read by this tool using the snippet :\n\n{\n"
                        "# import pickle\n"
                        "with open('trajectoire', 'rb') as pickle_file:\n"
                        "    array = pickle.load(pickle_file)\n}\n\n"
                        "Remember that your array must have 6 columns (3 positions + 3 rotations) but can have as many rows as you'd like."
                        )
                        self.bprint(pickle_help)
                        return
                    else:
                        self.bprint(f"The reading method {method} is unknown to this tool, please use one of npy, txt, csv, dat or pickle.", 1)
                        return


if __name__ == '__main__':
    # Command line arguments parsing
    parser = argparse.ArgumentParser(description='Command line frontend used to command cable driven robots.', epilog="This tool and the cable robot library were designed by student of the Ecole des Mines de Paris and all of the source code is available at [...] under the GPL 3 License.")

    parser.add_argument("--verbosity", choices=[0, 1, 2], default=2, help="The level of verbosity wanted from this tool. Default is 2, 1 means seing only warning and errors and 0 means only seing errors.")

    parser.add_argument("--unsafe", action='store_true', help="Control the robot in unsafe mode, only use if you know what you are doing!")

    parser.add_argument("--profile", default=None, help="A profile file describing the physical characteristics of the cable driven robot you are using. More informations can be found online.")

    parser.add_argument("--version", action='version', version="tool version 0.1")

    args = parser.parse_args()

    header = (
    "\n"
    "##########################################################################\n"
    "This tool and the cable robot library were designed by student of the\n"
    "Ecole des Mines de Paris and all of the source code is available at [...]\n"
    "under the GPL 3 License.\n"
    "##########################################################################\n"
    )
    print(header)

    cli = CLI(args)

    while True:
        try:
            command = input(">> ")
            cli.read_command(command)
        except EOFError:
            print("exit")  # In order to avoid ugly output
            cli.exit()
            break
