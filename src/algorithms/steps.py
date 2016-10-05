
def expregression(self, graph):
    regression_rate = 1/1000.0
    for v in graph.vs:
        diffx = (v["destination"][0] - v["coord"][0]) * regression_rate
        diffy = (v["destination"][1] - v["coord"][1]) * regression_rate
        v["coord"] = v["coord"][0] + diffx, v["coord"][1] + diffy
