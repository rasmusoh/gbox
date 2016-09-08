import math

max_size = 150
class Rule:

    def changeto(self, graph):
        pass

    #called when simulation start
    def simulate_start(self, graph, w, h):
        pass

    #called each frame
    def simulate_step(self, graph):
        pass


class KamadaKawaiRule(Rule):
    
    def __init__(self):
        self._regression_rate = 1/1000.0
        self.layout = None

    def simulate_start(self, graph, w, h):
        self.layout = graph.layout_kamada_kawai() 
        fill_p = .9
        dim = w* fill_p, h * fill_p
        self.layout.fit_into(dim)

    def simulate_step(self, graph):
        for v in graph.vs:
            diffx = (self.layout[v.index][0] - v["coord"][0]) * self._regression_rate
            diffy = (self.layout[v.index][1] - v["coord"][1]) * self._regression_rate
            v["coord"] = v["coord"][0] + diffx, v["coord"][1] + diffy

class EvcentRule(Rule):
    def changeto(self, graph):
        ecvents = graph.evcent()
        for v in graph.vs:
            v["size"] = ecvents[v.index]*max_size

class PageRankRule(Rule):
    def changeto(self, graph):
        ranks = graph.pagerank()
        for v in graph.vs:
            v["size"] = ranks[v.index]*max_size

class DegreeRule(Rule):
    def changeto(self, graph):
        degrees = graph.degree()
        maxd = max(degrees)
        for v in graph.vs:
            v["size"] = degrees[v.index]*max_size/maxd

class BetweennessRule(Rule):
    def changeto(self, graph):
        betweens = graph.betweenness()
        maxb = max(betweens)
        for v in graph.vs:
            v["size"] = betweens[v.index]*max_size/maxb

class ClosenessRule:
    def changeto(self, graph):
        closeness = graph.closeness()
        for v in graph.vs:
            v["size"] = closeness[v.index]*max_size

allrules = {
        "KAMADAKAWAI": KamadaKawaiRule(),
        "DEGREE": DegreeRule(),
        "EVCENT": EvcentRule(),
        "PAGERANK": PageRankRule(),
        "BETWEEN": BetweennessRule(),
        "CLOSENESS": ClosenessRule()
        } 

