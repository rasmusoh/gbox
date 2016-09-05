import Tkinter as tk
import growthmode
import math
from util import *

class RadialTreeMode(growthmode.GrowthMode):

    def _set_parameters_and_growthpattern(self):
        self.growthpattern = RadialTree
        self.add_int_parameter("nchildren", "Children", 2, 10, 2)
        self.add_double_parameter("len_alpha", "Length inc", 0, 3, 0.05, 1)
        self.add_bool_parameter("len_exp", "Length inc(is exp)")
        self.add_double_parameter("len_start", "Length start", 1, 200, 5, 50)
        self.add_double_parameter("tilt", "Tilt", -10, 10, 0.5, 0)
        self.add_int_parameter("startgen", "Start geneneration", -2, 2, 0)
        self.add_bool_parameter("closed_split", "Closed split")

class RadialTree(growthmode.GrowthPattern):

    '''
    how many generations to simulate, as a function of nchildren
    in order to keep tree generation fast. Ex: for nchildren=3, simulate 6 generations
    '''
    generations_for_nchildren = { 2 : 10, 3 : 6, 4 : 5, 5 : 4, 6 : 4, 7 : 3, 8 : 3, 9 : 3, 10: 3}

    def __init__(self, canvas, start, parameter_values):
        self.nchildren = parameter_values["nchildren"]
        self.len_alpha = parameter_values["len_alpha"]
        self.len_exp = parameter_values["len_exp"]
        self.len_start = parameter_values["len_start"]
        self.tilt = parameter_values["tilt"]
        self.closed_split = parameter_values["closed_split"]
        self.startgen =  parameter_values["startgen"]
        self.canvas = canvas
        self.activelayer = [RadialBranch(start, 0, self.len_start, self.startgen )]

        for i in range(0, self.generations_for_nchildren[self.nchildren]):
            self.branch(i+self.startgen)

    def branch(self, generation):
        newlayer = []
        spread = self.spread(generation)
        length = self.length(generation)
        for branch in self.activelayer:
            newlayer.extend(branch.branch(self.nchildren, length, spread, self.tilt))
        for branch in newlayer:
            self.canvas.create_line(branch.root[0], branch.root[1], branch.tip[0], branch.tip[1], tags="branch")
        self.activelayer = newlayer

    def length(self, generation):
        if self.len_exp:
            return self.len_start*(self.len_alpha**generation)
        else:
            return self.len_start*(generation**self.len_alpha)

    def spread(self, generation):
        if self.closed_split:
            return 2*math.pi/((self.nchildren)**(generation))
        else:
            return (2 + 1/self.nchildren)*math.pi/((self.nchildren)**(generation))

class RadialBranch:

    def __init__(self, root, direction, length, parentgeneration):
        self.root = root
        self.generation = parentgeneration + 1
        self.tip = endpoint(root, direction, length)
        self.direction = direction

    def branch(self, nchildren, length, spread, tilt):
        children = []
        for i in range(0, nchildren):
            children.append(RadialBranch(self.tip, self.child_direction(nchildren, i, spread, tilt), length, self.generation))
        return children

    def child_direction(self, n, i, spread, tilt):
        return self.direction + spread*(i - (n-1)/2.0 + tilt)/(n)



