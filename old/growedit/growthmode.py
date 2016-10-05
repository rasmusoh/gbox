import Tkinter as tk
import math

class GrowthMode:

    def __init__(self, configframe, canvas):
        self.canvas = canvas
        self.configframe = configframe
	self.parameters = []
        self.start = (500, 0)
        self._set_parameters_and_growthpattern()

    ## to be overridden by subclass
    def _set_parameters_and_growthpattern(self):
        self.growthpattern = GrowthPattern

    def set_start(self, start):
        self.start = start
        self.create_growth()

    def create_growth(self):
        self.clear()
        parameter_values = {parameter["name"] : parameter["var"].get() for parameter in self.parameters}
        self.growthpattern(self.canvas, self.start, parameter_values)

    def select(self):
	for widget in self.configframe.winfo_children():
	    widget.destroy()
        for i in range(0,len(self.parameters)):
            parameter = self.parameters[i]
            self.create_label(parameter, i)
            if parameter["type"] == "BOOL":
                self.create_checkbox(parameter, i)
            elif parameter["type"] == "INT":
                self.create_spinbox(parameter, i)
            elif parameter["type"] == "DOUBLE":
                self.create_entry(parameter, i)

    def add_bool_parameter(self, name, description, default = False):
        p = {"name" : name, "description" : description, "var" : tk.BooleanVar(), "type": "BOOL"} 
        p["var"].set(default)
        p["var"].trace('w', self.parameter_changed)
        self.parameters.append(p)

    def add_double_parameter(self, name, description , from_, to, step, default = 0):
        p = {"name" : name, "description" : description, "var" : tk.DoubleVar(), "type": "DOUBLE", "from": from_, "to": to, "step": step} 
        p["var"].set(default)
        p["var"].trace('w', self.parameter_changed)
        self.parameters.append(p)

    def add_int_parameter(self, name, description, from_, to, default = 0):
        p = {"name" : name, "description" : description, "var" : tk.IntVar(), "type": "INT", "from": from_, "to": to} 
        p["var"].set(default)
        p["var"].trace('w', self.parameter_changed)
        self.parameters.append(p)

    def create_spinbox(self, parameter, row):
        e = tk.Spinbox(self.configframe, from_=parameter["from"], to=parameter["to"], textvariable = parameter["var"])
        e.grid(column =1, row = row, sticky=tk.NW)

    def create_entry(self, parameter, row):
        e = tk.Entry(self.configframe, textvariable = parameter["var"])
        e.grid(column =1, row = row, sticky=tk.NW)

    def create_checkbox(self, parameter, row):
        e = tk.Checkbutton(self.configframe, textvariable=parameter["var"])
        e.grid(column =1, row = row, sticky=tk.NW)

    def create_label(self, parameter, row):
        e = tk.Label(self.configframe, text=parameter["description"])
        e.grid(column =0, row = row, sticky=tk.NW)

    def parameter_changed(self, *args):
        self.create_growth()

    def increase_param(self, index):
        if len(self.parameters) > index: 
            p = self.parameters[index]
            if p["type"] == "BOOL":
                p["var"].set(not p["var"].get())
            elif p["type"] == "INT":
                amount = min(p["var"].get() + 1, p["to"])
                p["var"].set(amount)
            elif p["type"] == "DOUBLE":
                amount = min(p["var"].get() + p["step"], p["to"])
                p["var"].set(amount)
    
    def decrease_param(self, index):
        if len(self.parameters) > index: 
            p = self.parameters[index]
            if p["type"] == "BOOL":
                p["var"].set(not p["var"].get())
            elif p["type"] == "INT":
                amount = max(p["var"].get() - 1, p["from"])
                p["var"].set(amount)
            elif p["type"] == "DOUBLE":
                amount = max(p["var"].get() - p["step"], p["from"])
                p["var"].set(amount)
    

    def clear(self):
        self.canvas.delete("branch")

class GrowthPattern:
    def __init__(self, canvas, start, parameter_values):
        pass


