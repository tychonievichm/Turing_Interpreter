import sys
import time

def run(): #main program
    #sys.argv.pop(0)
    code_file = 'test2.txt'#sys.argv.pop(0)
    input_string = '____1_1___1__1e'
    input_string = list(input_string)
    
    #['1']+['0']*4 + ['1']+['0']*3 + ['1']+['0']*4#sys.argv
    tape = ['_']*5 + input_string + ['_']*5
    #split tape into list
    head_position = 5
    machine_state = 'START'
    codeDict = read_code_to_dict(code_file)
    turing = machine(codeDict, tape, head_position, machine_state)
    turing.engage()
    
class code_line(object):
    def __init__(self,s):
        code_list = s.split(" ")
        self.key = " ".join(code_list[0:2])
        self.symbol = code_list[2]
        self.direction = code_list[3]
        self.state = code_list[4]
                 
                 
class machine(object):
    def __init__(self,codeDict, tape, head_position, machine_state):
        self.code = codeDict
        self.tape = tape
        self.position = head_position
        self.state = machine_state
        
    def read(self): #Gives the value that the head currently sees
        return self.tape[self.position]
    def write(self, new_symbol): #Head write in a new symbol to the current cell
        self.tape[self.position] = new_symbol
    def move(self, direction): #Head moves either left or right
        if direction == 'R':
            self.position += 1
        elif direction == 'L':
            self.position += -1
        else:
            print 'Invalid movement code.'
    def change_state(self, new_state):
        self.state = new_state
        
    def make_code_key(self):
        return " ".join([self.read(), self.state])
    
    def execute(self):
        code_key = self.make_code_key()
        if code_key in self.code:
            action = self.code[code_key]
            self.write(action.symbol)
            self.move(action.direction)
            self.change_state(action.state)
        else:
            print "Inescapable non-halting state attained."
    def engage(self):
        print " ".join(self.tape)
        print " "
        while self.state != 'HALT':
            time.sleep(.1)
            self.execute()
            tape_show = " ".join(self.tape)
            head_show = [" "] *len(tape_show)
            head_show[self.position] = "^"
            print self.state
            print " ".join(self.tape)
            print " ".join(head_show)
            print " "
            
def read_code_to_dict(file_name):
    f = open(file_name, "r")
    turing_code = f.read()
    f.close()
    turing_code =  turing_code.split("\n")
    turing_code = [s for s in turing_code if s[0] != '#']
    codeDict = dict()
    for s in turing_code: #convert code file into dict()
        c = code_line(s)
        codeDict[c.key] = c
    return codeDict



run()





