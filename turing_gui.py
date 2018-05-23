#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
#  Interface code for interacting with the Turing Machine simulator.    #
#                                                                       #
#########################################################################

import time

from Tkinter import *

import turing

class TuringGUI(object):
    def __init__(self, parent):
        self.parent = parent   
        self.container = Frame(parent)
        self.container.pack(side = TOP)
        self.buffer_frame_1 = BufferFrame(self.container, 40, 1, TOP)
        self.state_display_frame = StateFrame(self.container)
        self.tape_display_frame = TapeFrame(self.container)
        self.pointer_frame = PointerFrame(self.container)
        self.buffer_frame_2 = BufferFrame(self.container, 25, 1, TOP)
        self.interface_frame = InterfaceFrame(self.container)
        self.buffer_frame_3 = BufferFrame(self.container, 40, 1, TOP)

    def update_display(self):
        pos = self.machine.position
        tape_label_text = " ".join(self.machine.tape[pos-17:pos+16])
        self.tape_display_frame.tape_display.config(text=tape_label_text)
        self.state_display_frame.state_display.config(text=self.machine.state)     
        
        
class BufferFrame(object):
    def __init__(self, parent, ht, wd, sd):
        self.parent = parent
        self.container = Frame(parent, height=ht, width=wd)
        self.container.pack(side = sd, expand=False)


class StateFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack(side = TOP)       
        self.state_display = Label(self.container, text = "State.",
                                  font=("Courier", 12))  
        self.state_display.pack(side = TOP)   


class TapeFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack(side = TOP)
        self.tape_display = Label(self.container, text = "Machine tape.",
                                  font=("Courier", 12))   
        self.tape_display.pack(side = TOP)


class PointerFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack(side = TOP)
        self.tape_display = Label(self.container, text = "^",
                                  font=("Courier", 12))   
        self.tape_display.pack(side = TOP)


class InterfaceFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack(side = LEFT)
        self.file_frame = FileFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1,230, LEFT)
        self.control_frame = ControlFrame(self.container)
        

class FileFrame(object):
    def __init__(self, parent):
        self.my_parent = parent   
        self.container = Frame(parent)
        self.container.pack(side = LEFT)
        self.label_frame = self.LabelFrame(self.container)
        self.textbox_frame = self.TextboxFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1,10, LEFT)
        self.button_frame = self.ButtonFrame(self.container)
        
    class LabelFrame(object):
        def __init__(self, parent):
            self.container = Frame(parent)
            self.container.pack(side=LEFT)
            self.my_parent = parent
        
            self.input_label = Label(self.container, text = "Input", justify = RIGHT)   
            self.input_label.pack(side = TOP)
            self.file_label = Label(self.container, text = "File name", justify = RIGHT)   
            self.file_label.pack(side = TOP)
        
    class TextboxFrame(object):
        def __init__(self, parent):
            self.container = Frame(parent)
            self.container.pack(side=LEFT)
            self.parent = parent

            self.input_text = Text(self.container, height = 1, width = 30)
            self.input_text.insert(END, "____0____1___e")
            self.input_text.pack(side = TOP)
            self.file_text = Text(self.container, height = 1, width = 30)   
            self.file_text.insert(END, "test2.txt")
            self.file_text.pack(side = TOP)
        
    class ButtonFrame(object):
        def __init__(self, parent):
            self.container = Frame(parent)
            self.container.pack(side=LEFT)
            self.parent = parent
            self.load_button = Button(self.container, command = self.load_code)   
            self.load_button.configure(text="Load")
            self.load_button.pack(side = LEFT)
            
        def load_code(self):
            file_name = (app.interface_frame.file_frame.textbox_frame
                         .file_text.get("1.0",'end-1c'))
            input_string = (app.interface_frame.file_frame.textbox_frame
                            .input_text.get("1.0",'end-1c'))
            app.machine = turing.new_machine(file_name, input_string)

class ControlFrame(object):
    def __init__(self, parent):
        self.container = Frame(parent)
        self.container.pack(side=LEFT)
        self.parent = parent
        
        self.execute_button = Button(self.container, command = self.run_code)   
        self.execute_button.configure(text="Execute", background = "green")
        self.execute_button.pack(side = LEFT)
        
        self.step_button = Button(self.container, command = self.step_code, background = "yellow")   
        self.step_button.configure(text = "Step", background = "yellow")
        self.step_button.pack(side = LEFT)
        
        self.quit_button = Button(self.container, command = self.quit_code, background = "red")   
        self.quit_button.configure(text = "Quit", background = "red")
        self.quit_button.pack(side = LEFT)

    def run_code(self):
        if hasattr(app, 'machine'):
            while True:
                self.step_code()
                root.update()
                time.sleep(.1)
                if app.machine.state == "HALT":
                    break

                
    def step_code(self):
        if hasattr(app, 'machine'):
            if app.machine.state != "HALT":
                app.machine.step()
                app.update_display()
                
    def quit_code(self):
        root.destroy()



root = Tk()
root.title("Turing Machine Simulator")
app = TuringGUI(root)
# root.iconbitmap('uparrow.ico')
root.mainloop()