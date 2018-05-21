# -*- coding: utf-8 -*-
import sys
import time


def Run():  # main program

    code_file = 'test2.txt'
    input_string = '__0__1_1___1_0_1__e'
    input_string = list(input_string)
    tape = ['_']*5 + input_string + ['_']*5
    head_position = 5
    machine_state = 'START'
    code_dict = ReadCodeToDict(code_file)
    turing = Machine(code_dict, tape, head_position, machine_state)
    turing.Engage()


class CodeLine(object):
    def __init__(self, s):
        code_list = s.split(" ")
        self.key = " ".join(code_list[0:2])
        self.symbol = code_list[2]
        self.direction = code_list[3]
        self.state = code_list[4]


class Machine(object):
    def __init__(self, codeDict, tape, head_position, machine_state):
        self.code = codeDict
        self.tape = tape
        self.position = head_position
        self.state = machine_state

    def Read(self):  # Gives the value that the head currently sees
        return self.tape[self.position]

    def Write(self, new_symbol):  # Head write in a new symbol to the current cell
        self.tape[self.position] = new_symbol

    def Move(self, direction):  # Head moves either left or right
        if direction == 'R':
            self.position += 1
        elif direction == 'L':
            self.position += -1
        else:
            print 'Invalid movement code.'

    def ChangeState(self, new_state):
        self.state = new_state

    def MakeCodeKey(self):
        return " ".join([self.Read(), self.state])

    def ExecuteNextInstruction(self):
        code_key = self.MakeCodeKey()
        if code_key in self.code:
            action = self.code[code_key]
            self.Write(action.symbol)
            self.Move(action.direction)
            self.ChangeState(action.state)
        else:
            print "Inescapable non-halting state attained."

    def Engage(self):
        print " ".join(self.tape)
        print " "
        while self.state != 'HALT':
            time.sleep(.05)
            self.ExecuteNextInstruction()
            tape_show = " ".join(self.tape)
            head_show = [" "] * len(tape_show)
            head_show[self.position] = "^"
            print self.state
            print " ".join(self.tape)
            print " ".join(head_show)
            print " "


def ReadCodeToDict(file_name):
    f = open(file_name, "r")
    turing_code = f.read()
    f.close()
    turing_code = turing_code.split("\n")
    code_dict = {CodeLine(s).key: CodeLine(s)
                for s in turing_code if s[0] != '#'}
    return code_dict


Run()
