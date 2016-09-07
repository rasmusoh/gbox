import random
import math

standard_node_size = 10
snap_dist = 2550

class Mode:

    def __init__(self, canvas, graph, modvar):
        self._canvas = canvas
        self._graph = graph
        self._modvar = modvar
        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, "from" : None, "to" : None}

    def _create_vertex(self, coord, size = standard_node_size):
        self._graph.add_vertex(coord= coord, size = size)
        return self._graph.vs[len(self._graph.vs)-1]

    def _create_edge(self, fromv, tov):
        self._graph.add_edge(fromv, tov)

    def _get_closest_vertex(self, x, y):
        shape = self._canvas.find_closest(x, y)[0]
        tags = self._canvas.gettags(shape)
        if "vertex" in tags:
            vertex_id =  int(tags[1])
            return self._graph.vs[vertex_id]

    def _distance2(self, coord1, coord2):
        return (coord2[0]- coord1[0])**2 + (coord2[1] - coord1[1])**2

    def _reset_drag(self):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["from"] = None
        self._drag_data["to"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def mouse_release(self, event):
        self._reset_drag()

    def bg_click(self, event):
        pass
    def vertex_click(self, event):
        pass
    def mouse_move(self, event):
        pass

class AddMode(Mode):

    def bg_click(self, event):
        self._drag_data["item"] = self._create_vertex((event.x, event.y))
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def vertex_click(self, event):
        self._drag_data["item"] =  self._get_closest_vertex(event.x, event.y)
        self._drag_data["x"] = event.x 
        self._drag_data["y"] = event.y 

    def mouse_move(self, event):
        if self._drag_data["item"] != None:
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            dist =math.sqrt(delta_x**2 + delta_y**2)
            self._drag_data["item"]["size"] = standard_node_size + dist/2

class MoveMode(Mode):

    def vertex_click(self, event):
        self._drag_data["item"] = self._get_closest_vertex(event.x, event.y)
        self._drag_data["x"] = event.x - self._drag_data["item"]["coord"][0] 
        self._drag_data["y"] = event.y - self._drag_data["item"]["coord"][1]

    def mouse_move(self, event):
        if self._drag_data["item"] != None:
            self._drag_data["item"]["coord"] = (event.x - self._drag_data["x"], 
                                                event.y - self._drag_data["y"])

class ConnectMode(Mode):

    def mouse_release(self, event):
        if self._drag_data["from"] != None:
            self._canvas.delete(self._drag_data["item"])
            if self._drag_data["to"] != None:
                self._create_edge(self._drag_data["from"], self._drag_data["to"])
        self._reset_drag()

    def vertex_click(self, event):
        self._drag_data["from"] = self._get_closest_vertex(event.x, event.y)
        self._drawLine(event.x, event.y)

    def mouse_move(self, event):
        if self._drag_data["item"] != None:

            self._canvas.delete(self._drag_data["item"])

            to = self._get_closest_vertex(event.x, event.y)
            if to != None and self._distance2(to["coord"], (event.x, event.y)) <= snap_dist2:
                self._drag_data["to"] = to
                self._drawLine(to["coord"][0], to["coord"][1])
            else:
                self._drag_data["to"] = None 
                self._drawLine(event.x, event.y)

    def _drawLine(self, toX, toY):
        fromX, fromY = self._drag_data["from"]["coord"] 
        self._drag_data["item"] = self._canvas.create_line(fromX, fromY, toX, toY)

class EraseMode(Mode):
    pass

class TreeMode(Mode):
    pass

class BarabasiMode(Mode):

    def bg_click(self, event):
        new = self._create_vertex((event.x, event.y))
        new_index = len(self._graph.vs) -1
        weights = self._graph.degree() ##newly created has degree zero = can't select yourself
        for i in range(0, min(self._modvar.get(),new_index)):
            choice = self.weighted_choice(weights)
            self._create_edge(new_index,choice)
            weights[choice] = 0 ## cant select same again

    def weighted_choice(self, weights):
       total = sum(weights)
       r = random.uniform(0, total)
       upto = 0
       for w in range(0, len(weights)):
          if upto + weights[w] >= r:
             return w
          upto += weights[w]
       print weights, r, upto
       assert False, "Shouldn't get here"

class NeighbourMode(Mode):
    def bg_click(self, event):
        new = self._create_vertex((event.x, event.y))
        for i in range(0, self._modvar.get()):
            self.connect_nn(new)

    def vertex_click(self, event):
        vertex =  self._get_closest_vertex(event.x, event.y)
        for i in range(0, self._modvar.get()):
            self.connect_nn(vertex)

    def connect_nn(self, vertex):
        mindist = float("inf")
        nn = None
        for neighbour in self._graph.vs:
            dist = self._distance2(vertex["coord"], neighbour["coord"])
            if dist < mindist and self.possible_new_neighbours(vertex, neighbour):
                nn = neighbour
                mindist = dist

        if nn !=None:
            self._create_edge(vertex.index, nn.index)

    def possible_new_neighbours(self, from_, to):
        p =from_.index != to.index and not self._graph.are_connected(from_.index, to.index)
        return p
