import math

class Rule:
    def _simulate_step(self, graph):
        pass

class DegreeRule:
    
    def __init__(self):
        self._regression_rate = 1/1000.0

    def simulate_step(self, graph):
        for v in graph.vs:
            diff =  (10 + 25*v.degree()**2 - v["size"]) * self._regression_rate
            v["size"] += diff
