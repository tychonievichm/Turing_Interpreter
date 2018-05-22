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
    f.close()
    turing_code = turing_code.split("\n")
    code_dict = {_CodeLine(s).key: _CodeLine(s)
                 for s in turing_code if s[0] != '#'}
    return code_dict


class _CodeLine(object):
    """Defines format for reading code from a file."""
    def __init__(self, s):
        code_list = s.split(" ")
        self.key = " ".join(code_list[0:2])
        self.symbol = code_list[2]
        self.direction = code_list[3]
        self.state = code_list[4]


class Machine(object):
    """Methods and properties for a simulated Turing Machine."""
    def __init__(self, code_dict, tape, head_position, machine_state):
        self._code = code_dict
        self.tape = tape
        self.position = head_position
        self.state = machine_state

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
        else:
            raise DirectionError(direction)

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
        if code_key in self._code:
            action = self._code[code_key]
            self._write(action.symbol)
            self._move(action.direction)
            self._change_state(action.state)
        else:
            raise CodeError(self.read(), self.state)
        if len(self.tape) < self.position + 50:
            self.tape = self.tape + ['_']*100
        if self.position < 50:
            self.tape = ['_']*100 + self.tape
            self.position = self.position + 100


class CodeError(Exception):
    """Raised when no code exists for a given state"""
    def __init__(self, symbol, state):
        print {"No instruction for tape symbol {0} in state {1} found."
               .format(unicode(self.symbol, "utf-8"),
                       unicode(self.state, "utf-8"))
               }


class DirectionError(Exception):
    """Raised when an invalid direction instruction is given."""
    def __init__(self, bad_direction):
        print {("{0} is not a valid direction code.  Please make sure "
                "that all direction codes are either R or L.")
               .format(unicode(self.symbol, "utf-8"))
               }







