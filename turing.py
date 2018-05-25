#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
# Defines Machine class for Turing machine simulation, and gives and    #
# initialization method new_machine() for creating a Machine from code. #
# A valid code file with have comments marked by #, and code lines      #
# formatted as                                                          #
#                                                                       #
# <read_symbol> <machine_state> <write_symbol> <next_move> <next_state> #
#                                                                       #
# with spaces used as delimiters and valid moves being either R or L.   #
# The order of code lines is unimportant.  The initial state of a       #
# machine will always be START and the only accepted halting state      #
# is HALT.                                                              #
#                                                                       #
# Any interaction with a Machine object should be through its           #
# constructor, the new_machine function, the attributes                 #
# tape, position, and state, or its read() and step() methods.          #
#                                                                       #
# This module also contains a translator UgarteCode.make_tur_file to    #
# change code files in the format of Martin Ugarte's                    #
# turingmachinesimulator.com to the format used by this simulator.      #
# Check out this site for some extra sample TUring codes!               #
#                                                                       #
#########################################################################
#                                                                       #
#      Michael Tychonievich, Ph.D.                  May 24, 2018        #
#      Erdős Institute Cőde Bootcamp at The Ohio State University       #
#                                                                       #
#########################################################################


def new_machine(file_name, input_string):
    """Create a new Machine object from input data.

    Takes file indicated by file_name and converts it into a dictionary
    according to the format specifiedby the CodeLine() and by
    _read_code_to_dict, then initializes other parts of the Machine
    with default settings.
    """
    input_string = list(input_string)
    tape = ['_']*100 + input_string + ['_']*100
    machine_state = 'START'
    head_position = 100
    code_dict = _read_code_to_dict(file_name)
    return Machine(code_dict, tape, head_position, machine_state)


def _read_code_to_dict(file_name):
    """Convert a text file into a dictionary of CodeLines."""
    f = open(file_name, "r")
    turing_code = f.read()
    # If IOError is raised here, the program quits.
    f.close()
    turing_code = turing_code.split("\n")
    turing_code = {s for s in turing_code if s.strip() != "" and s[0] != '#'}
    # Remove comments and blank lines.
    code_dict = {_CodeLine(s).key: _CodeLine(s) for s in turing_code}
    if " " in code_dict.keys():
        code_dict.pop(" ")
    return code_dict


class _CodeLine(object):
    """Defines format for reading code from a file."""
    def __init__(self, s):
            code_list = s.split(" ")
            if len(code_list) >= 5:
                # Check to see if a line has enough information in it.
                # s.split(" ") usually has an extra empty string at the
                # end, and there might be comments that pad the length.
                self.key = " ".join(code_list[0:2])
                self.symbol = code_list[2]
                self.direction = code_list[3]
                self.state = code_list[4]
            else:
                self.key = " "
                self.symbol = " "
                self.direction = " "
                self.state = " "
                # These are placeholder values that cannot show up
                # otherwise.  This code line will be deleted before
                # the code dictionary is made into a Machine.


class Machine(object):
    """Methods and properties for a simulated Turing Machine."""
    def __init__(self, code_dict, tape, head_position, machine_state):
        self._code = code_dict
        self.tape = tape
        self.position = head_position
        self.state = machine_state
        self.error = False
        # self.error is True when an the machine enters a non-halting
        # state for which there is no instruction.  It does not attempt
        # to determine whether this is caused by a problem with the code
        # file or if the machine merely rejected the input since these
        # are technically the same thing.

    def read(self):
        """Returns the symbol currently seen by the head."""
        return self.tape[self.position]

    def _write(self, new_symbol):
        """Causes the current symbol to be overwritten by new_symbol."""
        self.tape[self.position] = new_symbol

    def _move(self, direction):
        """Causes the head to either the right or the left."""
        if direction == 'R':
            self.position += 1
        elif direction == 'L':
            self.position += -1
        elif direction == 'N':
            pass
        else:
            self.error = True
            raise DirectionError(direction + " is not a valid direction "
                                 "instruction.  Please make sure that all "
                                 "direction instructions are either R, L, "
                                 "or N.")

    def _change_state(self, new_state):
        """Causes the state of the Machine to change to new_state."""
        self.state = new_state

    def _make_code_key(self):
        """Create a key for use with the Machine's code dictionary.

        This method must respect the format defined by class _CodeLine.
        """
        return " ".join([self.read(), self.state])

    def step(self):
        """Look up instruction in the dictionary and execute it.

        Some minor exception handling is included, as well as a test to make
        sure that the end of the tape is never visible.
        """
        code_key = self._make_code_key()
        try:
            action = self._code[code_key]
            self._write(action.symbol)
            self._move(action.direction)
            self._change_state(action.state)
        except KeyError:
            self.error = True
        if len(self.tape) < self.position + 50:
            self.tape = self.tape + ['_']*100
        if self.position < 50:
            self.tape = ['_']*100 + self.tape
            self.position = self.position + 100


class UgarteCode(object):
    """Object that gathers and holds all of the code information
    from a text file holding Turing machine code in the Ugarte format.
    The method make_tur_file() writes this code in the appropriate
    format for the new_machine() function.
    """
    def __init__(self, file_name):
        f = open(file_name, "r")
        self.raw_lines = (f.read()).split("\n")
        f.close()
        self.get_metadata()
        self.translate_lines()

    def get_metadata(self):
        """Pull the metadata out of the file.  This determines
        the file name used by make_tur_file() as well as what
        states should be considered equivalent to START or HALT.
        """
        for s in self.raw_lines:
            init_check = (s.split(":")[0]).lower()
            if init_check == "name":
                self.name = "".join(s.split(":")[1:]).lower()
                self.name = filter(str.isalnum, self.name) + "_U.tur"
                # Formatting the given name so that it can be a file name.
            elif init_check == "init":
                self.init = (s.split(":")[1]).strip()
            elif init_check == "accept":
                # accepting states are given as a comma-delimited list,
                # so it gets pulled apart here
                seps = [",", ":"]
                self.accept = s
                for t in seps:
                    self.accept.replace(t, " ")
                self.accept = self.accept.split(" ")
                self.accept = [t.strip() for t in self.accept]
                self.accept.pop(0)

    def translate_lines(self):
        """Takes the list of lines in the input file and
        classifies each line as either a comment line or a code
        line.  Comment lines have '#' appended, while code
        lines are reformatted for use in constructing _CodeLine
        objects.
        """
        self.turing_code = ["# -*- coding: utf-8 -*-"]
        self.turing_code.append("")
        for s in self.raw_lines:
            if s.strip() == "":
                self.turing_code.append(s)
            elif s[0] == "/":
                self.turing_code.append("# " + s)
                # Comment out comments.
            elif s.split(":")[0] in ["name", "init", "accept"]:
                self.turing_code.append("# " + s)
                # Comment out metadata.
            elif len(s.split(",")) == 3:
                pass
                # Skip a line if it looks like the second line of
                # an instruction.
            elif len(s.split(",")) == 2:
                code_line_1 = s.split(",")
                code_line_2 = self.raw_lines[self.raw_lines.index(s)
                                             + 1].split(",")
                self.turing_code.append(self._convert_code(code_line_1
                                                           + code_line_2))
                # Include reformatted code line as code.
            else:
                self.turing_code.append("# BAD LINE " + s)
                # Comment out anything else and leave a warning in
                # the new file.  Any line marked as bad in the new 
                # code file should be reviewed if the code does not
                # behave as expected.

    def _convert_code(self, code_line):
        """Reformat a recognized instruction."""
        state_in = code_line[0].strip()
        tape_read = code_line[1].strip()
        state_out = code_line[2].strip()
        tape_write = code_line[3].strip()
        direction = code_line[4].strip()
        try:
            state_in = self._state_fix(state_in)
            state_out = self._state_fix(state_out)
            direction = self._direction_fix(direction)
        except AttributeError:
            raise MetadataError("Metadata not found.  Please run get_metadata")
        return " ".join([tape_read, state_in, tape_write,
                         direction, state_out])

    def _state_fix(self, state):
        """Change all init and accept states into 'START'
        and 'HALT' respectively.
        """
        if state == self.init:
            return "START"
        elif state in self.accept:
            return "HALT"
        else:
            return state

    def _direction_fix(self, direction):
        """Change direction instructions to the recognized symbols."""
        if direction == ">":
            return "R"
        elif direction == "<":
            return "L"
        else:
            return "N"

    def make_tur_file(self):
        """Takes the processed code and writes it to a file."""
        f = open("codes/" + self.name, 'w+')
        for s in self.turing_code:
            f.write(s + "\n")
        f.close()


class DirectionError(Exception):
    """Raised when an invalid direction instruction is given.  Untested."""
    pass


class MetadataError(Exception):
    """Raised when code metadata is looked for and not found."""
    pass
