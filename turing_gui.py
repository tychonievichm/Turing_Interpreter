#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
#  Interface code for interacting with the Turing Machine simulator.    #
#                                                                       #
#########################################################################

import Tkinter as tk  # or from Tkinter import *

import turing


class TuringGUI(object):
    def __init__(self, parent):
        self.stop = False
        self.wait_time = 150
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.buffer_frame_1 = BufferFrame(self.container, 40, 1, tk.TOP)
        self.state_display_frame = StateFrame(self.container)
        self.tape_display_frame = TapeFrame(self.container)
        self.pointer_frame = PointerFrame(self.container)
        self.buffer_frame_2 = BufferFrame(self.container, 25, 1, tk.TOP)
        self.interface_frame = InterfaceFrame(self.container)
        self.buffer_frame_3 = BufferFrame(self.container, 40, 1, tk.TOP)

    def update_display(self):
        pos = self.machine.position
        tape_label_text = " ".join(self.machine.tape[pos-17:pos+16])
        self.tape_display_frame.tape_display.config(text=tape_label_text)
        self.state_display_frame.state_display.config(text=self.machine.state)


class BufferFrame(object):
    def __init__(self, parent, ht, wd, sd):
        self.container = tk.Frame(parent, height=ht, width=wd)
        self.container.pack(side=sd, expand=False)


class StateFrame(object):
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.state_display = tk.Label(self.container, text="Please initialize",
                                      font=("Courier", 12))
        self.state_display.pack(side=tk.TOP)


class TapeFrame(object):
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.tape_display = tk.Label(self.container, text="the Machine.",
                                     font=("Courier", 12))
        self.tape_display.pack(side=tk.TOP)


class PointerFrame(object):
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.TOP)
        self.tape_display = tk.Label(self.container, text="^",
                                     font=("Courier", 12))
        self.tape_display.pack(side=tk.TOP)


class InterfaceFrame(object):
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.LEFT)
        self.file_frame = FileFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1, 50, tk.LEFT)
        self.slider_frame = SliderFrame(self.container)
        self.buffer_frame = BufferFrame(self.container, 1, 50, tk.LEFT)
        self.control_frame = ControlFrame(self.container)


class FileFrame(object):
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
            self.input_label = tk.Label(self.container, text="Input")
            self.input_label.pack(side=tk.TOP)
            self.file_label = tk.Label(self.container, text="File name")
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
            self.container = tk.Frame(parent)
            self.container.pack(side=tk.LEFT)
            self.load_button = tk.Button(self.container,
                                         command=self.load_code,
                                         background="gray", text="Load")
            self.load_button.pack(side=tk.LEFT)

        def load_code(self):
            file_name = (app.interface_frame.file_frame.textbox_frame
                         .file_text.get("1.0", 'end-1c'))
            input_string = (app.interface_frame.file_frame.textbox_frame
                            .input_text.get("1.0", 'end-1c'))
            app.machine = turing.new_machine(file_name, input_string)
            app.update_display()
            app.stop = False


class SliderFrame(object):
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.LEFT)
        self.slider = tk.Scale(self.container, from_=0, to=300,
                               orient=tk.HORIZONTAL,
                               command=self.update_wait_time,
                               label="Delay between steps(ms)", resolution = 10,
                               length=150)
        self.slider.pack(side=tk.TOP)
        self.slider.set(150)

    def update_wait_time(self, slider_value):
        app.wait_time = slider_value


class ControlFrame(object):
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(side=tk.LEFT)
        self.execute_button = tk.Button(self.container, command=self.run_code,
                                        background="green", text="Execute")
        self.execute_button.pack(side=tk.LEFT)
        self.step_button = tk.Button(self.container, command=self.step_code,
                                     background="yellow", text="Step")
        self.step_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.container, command=self.stop_code,
                                     background="red", text="Stop")
        self.stop_button.pack(side=tk.LEFT)

    def run_code(self):
        if hasattr(app, 'machine'):
            self.step_code()
            root.update()
            if app.machine.state == "HALT":
                return
            elif app.stop is False:
                root.after(app.wait_time, self.run_code)
            elif app.stop is True:
                app.stop = False

    def step_code(self):
        if hasattr(app, 'machine'):
            if app.machine.state != "HALT":
                app.machine.step()
                app.update_display()
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
