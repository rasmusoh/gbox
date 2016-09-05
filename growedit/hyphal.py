import Tkinter as tk
import growthmode
import math
import random
from util import *


class HyphalMode(growthmode.GrowthMode):
    def _set_parameters_and_growthpattern(self):
        self.add_int_parameter("supress", "Neighbours to supress branching", 1, 100, 2)
        self.add_int_parameter("kill", "Neighbours to kill tip", 1, 100, 5)
        self.add_double_parameter("neighbour_r", "Neighbour sensing radius", 1, 200, 1, 100)
        self.add_bool_parameter("random", "Randomize")
        self.add_double_parameter("stepsize", "Step size", 1, 100, 1, 10)
        self.add_int_parameter("steptotal", "Number of steps", 100, 10000, 100)
        self.add_int_parameter("maxnotips", "Max number of tips", 100, 5000, 1000)
        self.growthpattern = HyphalGrowth

class HyphalGrowth(growthmode.GrowthPattern):

    def __init__(self, canvas, start, pv):
        self.random = pv["random"]
        self.canvas = canvas
        self.activetips = [HyphalTip(start, pv["neighbour_r"]**2, pv["supress"], pv["kill"], 0, pv["maxnotips"])]

        stepsize = pv["stepsize"]
        steptotal = pv["steptotal"]

        for i in range(0, steptotal):
            newlayer = []
            for tip in self.activetips:
                newlayer.extend(tip.step(stepsize, self.activetips))
            for tip in self.activetips:
                self.canvas.create_line(tip.lastpos[0], tip.lastpos[1], tip.pos[0], tip.pos[1], tags="branch")
            self.activetips = newlayer

class HyphalTip:

    def __init__(self, position, neighbour_r2, supress, kill, direction, maxnotips):
        self.pos = position
        self.lastpos= position
        self.neighbour_r2 = neighbour_r2
        self.supress = supress
        self.kill = kill
        self.direction = direction
        self.maxnotips = maxnotips

    def step(self, size, othertips):
        self.lastpos = self.pos
        self.pos = endpoint(self.pos, self.direction, size)
        if len(othertips) < self.maxnotips and self.neighbours(othertips)  < self.supress:
            direction = self.direction + random.uniform(-math.pi/2, math.pi/2)
            return [self, HyphalTip(self.pos, self.neighbour_r2, self.supress, self.kill, direction, self.maxnotips)]
        elif self.neighbours(othertips)  < self.kill:
            return [self]
        return []

    def neighbours(self, othertips):
        n_neighbours = 0
        for other in othertips:
            if distance2(self.pos, other.pos) < self.neighbour_r2:
                n_neighbours+=1
        return n_neighbours

class PushHyphalMode(growthmode.GrowthMode):
    def _set_parameters_and_growthpattern(self):
        self.add_double_parameter("influence_constant", "Influence constant", 1, 100, 1, 2)
        self.add_double_parameter("supress", "Neighbours to supress branching", 1, 100, 1, 2)
        self.add_double_parameter("kill", "Neighbours to kill tip", 1, 100, 1, 5)
        self.add_double_parameter("stepsize", "Step size", 1, 100, 1, 10)
        self.add_int_parameter("steptotal", "Number of steps", 100, 10000, 100)
        self.add_int_parameter("maxnotips", "Max number of tips", 100, 5000, 1000)
        self.growthpattern = PushHyphalGrowth

class PushHyphalGrowth(growthmode.GrowthPattern):

    def __init__(self, canvas, start, pv):
        self.canvas = canvas
        self.activetips = [PushHyphalTip(start, [10,10], pv["maxnotips"], pv["supress"], pv["kill"], pv["influence_constant"])]

        stepsize = pv["stepsize"]
        steptotal = pv["steptotal"]

        for i in range(0, steptotal):
            for tip in self.activetips:
                self.activetips.extend(tip.step(stepsize, self.activetips))
            for tip in self.activetips:
                self.canvas.create_line(tip.lastpos[0], tip.lastpos[1], tip.pos[0], tip.pos[1], tags="branch")


class PushHyphalTip:

    def __init__(self, position, velocity, maxnotips, supress, kill, influence_constant):
        self.pos = position
        self.lastpos= position
        self.velocity = velocity
        self.maxnotips = maxnotips
        self.supress = supress
        self.kill = kill
        self.influence_constant = influence_constant

    def step(self, size, othertips):
        self.lastpos = self.pos
        totalsize = self.get_neighbour_influence(othertips)
        self.pos = self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]
        if len(othertips) < self.maxnotips and totalsize < self.supress:
            return [self, PushHyphalTip(self.pos, self.velocity, self.maxnotips, self.supress, self.kill, self.influence_constant)]
        elif totalsize < self.kill:
            return [self]
        return []

    def get_neighbour_influence(self, othertips):
        totalsize = [0.0, 0.0]
        netforce = [0.0, 0.0]
        for other in othertips:
            d = (1 + distance2(self.pos, other.pos))
            forcex, forcey = vector(self.pos, other.pos)[0]/d, vector(self.pos, other.pos)[1]/d
            totalsize[0]+= math.fabs(forcex)
            totalsize[1]+=math.fabs(forcey)
            netforce[0]+=self.influence_constant*forcex
            netforce[1]+=self.influence_constant*forcey
        self.velocity[0]+=netforce[0]
        self.velocity[1]+=netforce[1]
        return totalsize[0]**2+ totalsize[1]**2

