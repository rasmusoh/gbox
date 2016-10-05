def evcent(self, graph):
    ecvents = graph.evcent()
    for v in graph.vs:
        v["size"] = ecvents[v.index]*150

def pagerank(self, graph):
    ranks = graph.pagerank()
    for v in graph.vs:
        v["size"] = ranks[v.index]*150

def degree(self, graph):
    degrees = graph.degree()
    maxd = max(degrees)
    for v in graph.vs:
        v["size"] = degrees[v.index]*150/maxd

def betweenness(self, graph):
    betweens = graph.betweenness()
    maxb = max(betweens)
    for v in graph.vs:
        v["size"] = betweens[v.index]*150/maxb

def closeness(self, graph):
    closeness = graph.closeness()
    for v in graph.vs:
        v["size"] = closeness[v.index]*150
