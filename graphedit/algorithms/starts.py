def kamada_kawai(self, graph, **kwargs):
    layout = graph.layout_kamada_kawai() 
    fill_p = .9
    w = kwargs.get('w', 900)
    h = kwargs.get('h', 900)
    dim = w* fill_p, h * fill_p
    layout.fit_into(dim)

    for v in graph.vs:
        v["destination"] = layout[v.index]
