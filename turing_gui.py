#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
# Interface code for interacting with the Turing Machine simulator.     #
# See the turing module for information on how the machine simulation   #
# works.                                                                #
#                                                                       #
#########################################################################
#                                                                       #
#      Michael Tychonievich, Ph.D.                  May 24, 2018        #
#      Erdős Institute Cőde Bootcamp at The Ohio State University       #
#                                                                       #
#########################################################################

import Tkinter as tk  # or from Tkinter import *

import turing


class TuringGUI(object):
    """The main object for the program.  It must be named app.

    self.stop is used to determine if the user has issued an order to
    stop, which causes the machine to finish the instruction it is on
    and not execute the next one.

    self.wait_time determines the minimum amount of time between steps.

    self.num_steps is the number of (attempted) executions since the
    most recent machine was loaded.

    self.machine is a Machine object defined in the turing module.
    This is initialized by the load button on the GUI.
    """
    def __init__(self, parent):
        self.stop = True
        self.wait_time = 150
        self.name = "Please load a text file containing Turing Machine code."
        self.num_steps = 0
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.buffer_frame_1 = BufferFrame(self.container, 10, 1, tk.TOP)
        self.name_display_frame = NameFrame(self.container)
        self.buffer_frame_1 = BufferFrame(self.container, 10, 1, tk.TOP)
        self.state_display_frame = StateFrame(self.container)
        self.tape_display_frame = TapeFrame(self.container)
        self.pointer_frame = PointerFrame(self.container)
        self.buffer_frame_2 = BufferFrame(self.container, 25, 1, tk.TOP)
        self.interface_frame = InterfaceFrame(self.container)
        self.buffer_frame_3 = BufferFrame(self.container, 40, 1, tk.TOP)

    def update_display(self):
        """Update the display when the machine runs one step."""
        pos = self.machine.position
        tape_label_text = " ".join(self.machine.tape[pos-19:pos+20])
        self.tape_display_frame.tape_display.config(text=tape_label_text)
        self.state_display_frame.state_display.config(text=self.machine.state)

    def load_name_display(self):
        """Update the display when a new machine is loaded."""
        self.name_display_frame.name_label.config(text="Program " +
                                                  self.name + " loaded.")

    def halt_name_display(self):
        """Update the display when a machine halts."""
        output = ("".join(self.machine.tape)).strip("_")
        halt_text = " Input accepted after "\
                    + str(app.num_steps) + " steps.  Output: " + output
        self.name_display_frame.name_label.config(text=halt_text)

    def step_name_display(self):
        """Updates the information display."""
        self.name_display_frame.name_label.config(text="Program " +
                                                  self.name + " after "
                                                  + str(app.num_steps)
                                                  + " steps.")

    def display_error(self):
        """If an input is rejected due to a KeyError in the turing module,
        this updates the information display to let the user know.
        """
        reject_text = " Input rejected after "\
                      + str(app.num_steps) + " steps.  No instruction for "\
                      + self.machine.read() + " found."
        self.name_display_frame.name_label.config(text=reject_text)


class BufferFrame(object):
    """Empty frame for spacing purposes."""
    def __init__(self, parent, ht, wd, sd):
        self.container = tk.Frame(parent, height=ht, width=wd)
        self.container.pack(side=sd, expand=False)


class NameFrame(object):
    """This is the information display for the machine.  It will usually
    contain the current machine's name, pulled out of the file name of
    the file used to load the current machine.
    """
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.name_label = tk.Label(self.container, text="Please load a "
                                   "text file containing Turing Machine "
                                   "code.", font=("Courier", 12))
        self.name_label.pack(side=tk.TOP)


class StateFrame(object):
    """This holds the label showing the machine's current state."""
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.state_display = tk.Label(self.container, text="Please initialize",
                                      font=("Courier", 12))
        self.state_display.pack(side=tk.TOP)


class TapeFrame(object):
    """This holds the label showing the machine's current tape near the
    read-write head.
    """
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.tape_display = tk.Label(self.container, text="the Machine.",
                                     font=("Courier", 12))
        self.tape_display.pack(side=tk.TOP)


class PointerFrame(object):
    """This holds the label showing the machine's read-write head
    It should line up with the currently viewed tape cell on the display.
    """
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.tape_display = tk.Label(self.container, text="^",
                                     font=("Courier", 12))
        self.tape_display.pack(side=tk.TOP)


class InterfaceFrame(object):
    """All of the interactive elements of the GUI are in this frame."""
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.LEFT)
        self.file_frame = FileFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1, 50, tk.LEFT)
        self.slider_frame = SliderFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1, 50, tk.LEFT)
        self.control_frame = ControlFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1, 20, tk.LEFT)


class FileFrame(object):
    """Holds textboxes for the user to place file name and input string
    to initialize a machine.  The user must select a format for the file
    using radio buttons, and press the load button to continue.  The
    other control buttons will not do anything until that happens!
    """
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.LEFT)
        self.label_frame = self.LabelFrame(self.container)
        self.textbox_frame = self.TextboxFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1, 10, tk.LEFT)
        self.button_frame = self.ButtonFrame(self.container)

    class LabelFrame(object):
        def __init__(self, parent):
            self.container = tk.Frame(parent)
            self.container.pack(side=tk.LEFT)
            self.input_label = tk.Label(self.container, text="Input",
                                        font=("Helvetica", 8))
            self.input_label.pack(side=tk.TOP)
            self.file_label = tk.Label(self.container, text="File name",
                                       font=("Helvetica", 8))
            self.file_label.pack(side=tk.TOP)

    class TextboxFrame(object):
        def __init__(self, parent):
            self.container = tk.Frame(parent)
            self.container.pack(side=tk.LEFT)
            self.input_text = tk.Text(self.container, height=1, width=30)
            self.input_text.insert(tk.END, "____0____1___e")
            self.input_text.pack(side=tk.TOP)
            self.file_text = tk.Text(self.container, height=1, width=30)
            self.file_text.insert(tk.END, "codes/test2.tur")
            self.file_text.pack(side=tk.TOP)

    class ButtonFrame(object):
        def __init__(self, parent):
            self.container1 = tk.Frame(parent)
            self.container1.pack(side=tk.TOP)
            self.select_label = tk.Label(self.container1,
                                         text="Select format, then load.",
                                         font=("Helvetica", 8))
            self.select_label.pack(side=tk.RIGHT)
            self.container2 = tk.Frame(parent)
            self.container2.pack(side=tk.TOP)
            self.load_button = tk.Button(self.container2,
                                         command=self.load_code,
                                         text="Load", height=1,
                                         font=("Helvetica", 8))
            self.load_button.pack(side=tk.LEFT)
            self.file_format = tk.IntVar()
            self.file_format.set(0)
            self.tur_button = tk.Radiobutton(self.container2,
                                             text=" .tur ",
                                             variable=self.file_format,
                                             value=0, height=1,
                                             indicatoron=1,
                                             font=("Helvetica", 8))
            self.tur_button.pack(side=tk.LEFT)
            self.Ugarte_button = tk.Radiobutton(self.container2,
                                                text="Ugarte",
                                                variable=self.file_format,
                                                value=1, height=1,
                                                indicatoron=1,
                                                font=("Helvetica", 8))
            self.Ugarte_button.pack(side=tk.LEFT)

        def load_code(self):
            """Loads the file and input indicated by the user."""
            file_name = (app.interface_frame.file_frame.textbox_frame
                         .file_text.get("1.0", 'end-1c'))
            input_string = (app.interface_frame.file_frame.textbox_frame
                            .input_text.get("1.0", 'end-1c'))
            if self.file_format.get() == 1:
                new_code = turing.UgarteCode(file_name)
                new_code.make_tur_file()
                file_name = "codes/" + new_code.name
            app.machine = turing.new_machine(file_name, input_string)
            app.name = (file_name.split("/").pop()).split(".").pop(0)
            app.load_name_display()
            app.update_display()
            app.stop = True
            app.num_steps = 0


class SliderFrame(object):
    """Holds a scale to determine how fast the machine will execute
    instructions.
    """
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.LEFT)
        self.slider = tk.Scale(self.container, from_=0, to=500,
                               orient=tk.HORIZONTAL,
                               command=self.update_wait_time,
                               label="Delay between steps(ms)",
                               resolution=10, length=150,
                               font=("Helvetica", 8))
        self.slider.pack(side=tk.TOP)
        self.slider.set(150)

    def update_wait_time(self, slider_value):
        app.wait_time = slider_value


class ControlFrame(object):
    """Holds buttons for the user to control machine behavior."""
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.LEFT)
        self.execute_button = tk.Button(self.container, command=self.run_code,
                                        background="green", text="Execute",
                                        font=("Helvetica", 8))
        self.execute_button.pack(side=tk.LEFT)
        self.step_button = tk.Button(self.container, command=self.step_code,
                                     background="yellow", text="Step",
                                     font=("Helvetica", 8))
        self.step_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.container, command=self.stop_code,
                                     background="red", text="Stop",
                                     font=("Helvetica", 8))
        self.stop_button.pack(side=tk.LEFT)

    def run_code(self):
        """Check to see whether or not the machine is already looping
        before starting a loop..
        """
        if app.stop is True:
            app.stop = False
            root.update()
            root.after(app.wait_time, self.run_code_loop)

    def run_code_loop(self):
        """Execute one instruction and display the results."""
        if hasattr(app, 'machine'):
            self.step_code()
            root.update()
            if app.machine.state == "HALT":
                app.halt_name_display()
                return
            elif app.stop is False:
                root.after(app.wait_time, self.run_code_loop)

    def step_code(self):
        """Execute one instruction and display the results."""
        if hasattr(app, 'machine'):
            if app.machine.error is True:
                app.stop = True
                app.display_error()
            elif app.machine.state != "HALT":
                app.machine.step()
                app.num_steps += 1
                app.update_display()
                app.step_name_display()
        else:
            app.state_display_frame.state_display.config(
                    text="Please initialize")
            app.tape_display_frame.tape_display.config(
                    text="the Machine.")

    def stop_code(self):
        app.stop = True


root = tk.Tk()
root.title("Turing Machine Simulator")
app = TuringGUI(root)
# root.iconbitmap('uparrow.ico')
root.mainloop()
