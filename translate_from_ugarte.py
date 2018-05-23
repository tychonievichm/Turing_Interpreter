#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
# This is a simple text analysis script that takes codes written in     #
# the format for Martin Ugarte's turingmachinesimulator.com and         #
# rewrites them in the format used in the turing module.                #
#                                                                       #
#########################################################################


def read_Ugarte(file_name):
    """Convert a code file in Ugarte's format.

    This takes a code file in Ugarte's format and changes it to the
    format used by the turing module.  Comments, special states, and
    instructions are all rewritten in the appropriate way, and the name
    specified by name: is used as the file name of the resulting .tur
    file.
    """
    f = open(file_name, "r")
    Ugarte_code = f.read()
    f.close()
    Ugarte_code = Ugarte_code.split("\n")
    turing_code = ["# -*- coding: utf-8 -*-"]
    for s in Ugarte_code:
        init_check = (s.split(":")[0]).lower()
        if init_check == "name":
            new_file_name = "".join(s.split(":")[1:]).lower()
            t = "#" + s
            turing_code.append(t)
        elif init_check == "init":
            old_START = (s.split(":")[1]).strip()
            t = "#" + s
            turing_code.append(t)
        elif init_check == "accept":
            old_seps = ["_", ",", ":"]
            old_HALT_list = s
            for i in [0, 1, 2]:
                old_HALT_list.replace(old_seps[i], " ")
            old_HALT_list = old_HALT_list.split(" ")
            old_HALT_list.pop(0)
            t = "#" + s
            turing_code.append(t)
        elif s.strip() == "":
            pass
        elif len(s.split(",")) == 3:
            pass
        elif s[0] == "/" and s[1] == "/":
            t = "#" + s
            turing_code.append(t)
        elif len(s.split(",")) == 2:
            code_1 = s.split(",")
            code_2 = Ugarte_code[Ugarte_code.index(s) + 1].split(",")
            t = _convert_code(code_1 + code_2, old_START, old_HALT_list)
            turing_code.append(t)
        else:
            print "bad Ugarte code line found"
            print s
    new_file_name = filter(str.isalnum, new_file_name) + ".tur"
    f = open("codes/" + new_file_name, 'w+')
    for s in turing_code:
        f.write(s + "\n")
    f.close()


def _convert_code(old_code_line, old_START, old_HALT_list):
    state_in = old_code_line[0]
    tape_read = old_code_line[1]
    state_out = old_code_line[2]
    tape_write = old_code_line[3]
    direction = old_code_line[4]
    
    def state_fix(state):
        if state == old_START:
            return "START"
        elif state in old_HALT_list:
            return "HALT"
        else:
            return state
    state_in = state_fix(state_in)
    state_out = state_fix(state_out)
    if direction == ">":
        direction = "R"
    elif direction == "<":
        direction = "L"
    else:
        direction = "N"
    return " ".join([tape_read, state_in, tape_write, direction, state_out])
