#!/usr/bin/env python.
# -*- coding: utf-8 -*-

##############################################################################
#                                                                            #
#    Interface code for interacting with the Turing Machine simulator.       #
#                                                                            #
##############################################################################

from Tkinter import *
import turing

class TuringGUI(object):
    def __init__(self, parent):
        self.parent = parent   
        self.container = Frame(parent)
        self.container.pack(side = TOP)
        self.buffer_frame_1 = BufferFrame(self.container, 40, 1, TOP)
        self.state_display_frame_frame = StateFrame(self.container)
        self.tape_display_frame = TapeFrame(self.container)
        self.pointer_frame = PointerFrame(self.container)
        self.buffer_frame_2 = BufferFrame(self.container, 25, 1, TOP)
        self.interface_frame = InterfaceFrame(self.container)
        self.buffer_frame_3 = BufferFrame(self.container, 40, 1, TOP)


class BufferFrame(object):
    def __init__(self, parent, ht, wd, sd):
        self.parent = parent
        self.container = Frame(parent, height=ht, width=wd)
        self.container.pack(side = sd, expand=False)


class StateFrame(object):
    def __init__(self, parent):
        self.container = Frame(parent)
        self.container.pack(side = TOP)
        state_display_text = Text(self.container, height=1, width=10)
        state_display_text.pack(side = TOP)
        state_display_text.insert(END, "Machine state goes here.")


class TapeFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack(side = TOP)
        self.tape_display_text = Text(self.container, height=1, width=100)
        self.tape_display_text.pack(side = TOP)
        self.tape_display_text.insert(END, "Machine tape goes here.")


class PointerFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack(side = TOP)
        self.pointer_text = Text(self.container, height=1, width=1)
        self.pointer_text.pack(side = TOP)
        self.pointer_text.insert(END, "^")


class InterfaceFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack(side = LEFT)
        self.file_frame = FileFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1,240, LEFT)
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
        
            self.input_label = Text(self.container, height = 1, width = 30)
            self.input_label.insert(END, "Input")
            self.input_label.pack(side = TOP)
            self.file_label = Text(self.container, height = 1, width = 30)   
            self.file_label.insert(END, "File name")
            self.file_label.pack(side = TOP)
        
    class ButtonFrame(object):
        def __init__(self, parent):
            self.container = Frame(parent)
            self.container.pack(side=LEFT)
            self.parent = parent
            self.load_button = Button(self.container, command = self.LoadCode)   
            self.load_button.configure(text="Load")
            self.load_button.pack(side = LEFT)
            
        def LoadCode(self):
            root.machine = turing.new_machine('test2.txt','____0____1___e')
            print "Machine loaded."
            
class ControlFrame(object):
    def __init__(self, parent):
        self.container = Frame(parent)
        self.container.pack(side=LEFT)
        self.parent = parent
        
        self.execute_button = Button(self.container, command = self.RunCode)   
        self.execute_button.configure(text="Execute", background = "green")
        self.execute_button.pack(side = LEFT)
        
        self.step_button = Button(self.container, command = self.StepCode, background = "yellow")   
        self.step_button.configure(text = "Step", background = "yellow")
        self.step_button.pack(side = LEFT)
        
        self.quit_button = Button(self.container, command = self.QuitCode, background = "red")   
        self.quit_button.configure(text = "Quit", background = "red")
        self.quit_button.pack(side = LEFT)

    def RunCode(self):
        print "Engage the Machine."
    def StepCode(self):
        print "Let the Machine take one step."
    def QuitCode(self):
        print "Shutting down the Machine."
        # root.destroy()



root = Tk()
app = TuringGUI(root)
# root.iconbitmap('alan_turing.ico')
root.mainloop()