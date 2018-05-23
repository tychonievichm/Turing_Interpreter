#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
# This is a simple text analysis script that takes codes written in     #
# the format for Martin Ugarte's turingmachinesimulator.com and         #
# rewrites them in the format used in the turing module.                #
#                                                                       #
#########################################################################


"""Convert a code file in Ugarte's format.

This takes a code file in Ugarte's format and changes it to the
format used by the turing module.  Comments, special states, and
instructions are all rewritten in the appropriate way, and the name
specified by name: is used as the file name of the resulting .tur
file.
"""


class UgarteCode(object):
    """Object that gathers and holds all of the code information
    from a text file holding Turing machine code in the Ugarte format.
    The method make_tur_file() writes this code in the appropriate
    format for the turing module.
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
            elif init_check == "init":
                self.init = (s.split(":")[1]).strip()
            elif init_check == "accept":
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
        lines are reformatted.
        """
        self.turing_code = ["# -*- coding: utf-8 -*-"]
        self.turing_code.append("")
        for s in self.raw_lines:
            if s.strip() == "":
                self.turing_code.append(s)
            elif len(s.split(",")) == 3:
                pass
            elif s[0] == "/" and s[1] == "/":
                self.turing_code.append("# " + s)
            elif s.split(":")[0] in ["name", "init", "accept"]:
                self.turing_code.append("# " + s)
            elif len(s.split(",")) == 2:
                code_line_1 = s.split(",")
                code_line_2 = self.raw_lines[self.raw_lines.index(s)
                                             + 1].split(",")
                self.turing_code.append(self._convert_code(code_line_1
                                                           + code_line_2))
            else:
                self.turing_code.append("# BAD LINE " + s)

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
            direction = "R"
        elif direction == "<":
            direction = "L"
        else:
            direction = "N"
        return direction

    def make_tur_file(self):
        """Takes the processed code and writes it to a file."""
        f = open("codes/" + self.name, 'w+')
        for s in self.turing_code:
            f.write(s + "\n")
        f.close()


class MetadataError(Exception):
    pass
