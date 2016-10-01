import numpy as np
import numpy.linalg
import igraph

class Mesh:
    def __init__(self, array, index):
        self.array = array
        self.index = index
        self.hasLines = False

    def combine(self, b):
        array = np.concatenate((self.array, b.array))
        index = np.concatenate((self.index, self.index.shape[0] + b.index))
        return Mesh(array, index)

    def add_lines(self, index):
        if not hasLines:
            hasLines = True
            linesStartIndex = self.index.shape[0] 
        self.index = np.concatenate((self.index, b.index))

class NetworkLineMesh:
    def __init__(self, smoothness, graph):
        self.circle_mesh = circle_mesh(smoothness)
        self.mesh = self.update_mesh(graph)

    def update_mesh(self, graph):
        self.mesh = verteces_mesh(graph, self.circle_mesh).add_lines(edges_line_index(graph, self.circle_mesh))

class NetworkThickMesh:
    def __init__(self, smoothness, width, graph):
        self.hw = width/2 
        self.circle_mesh = circle_mesh(smoothness)
        self.mesh = self.update_mesh(graph)

    def update_mesh(self, graph):
        self.mesh = verteces_mesh(graph, self.circle_mesh).combine(edges_triangle_mesh(graph, self.circle_mesh))

def verteces_mesh(graph, circle_mesh):
    return Mesh(verteces_array(graph, circle_mesh), verteces_index(graph, circle_mesh))

def verteces_array(graph, circle_mesh):
    positions = np.array(graph.vs["pos"], dtype = np.float32)
    sizes = np.array(graph.vs["size"], dtype = np.float32)
    ncircles = positions.shape[0]
    smoothness = circle_mesh.shape[0]

    pos_repeated = np.repeat(positions, smoothness, 0)
    size_repeated = np.repeat(sizes, smoothness)
    circle_tiled = np.tile(circle_mesh.array, (ncircles,1))

    return pos_repeated + (circle_tiled.T * size_repeated).T

def verteces_index(graph, circle_mesh):
    ncircles = len(graph.vs)
    smoothness = circle_mesh.shape[0]
    pos = np.arange(0, ncircles*smoothness, smoothness, dtype=ubyte)

    circle_tiled = np.tile(circle_mesh.index, (ncircles,1))
    pos_repeated =np.repeat(pos, ncircles)

    return circle_tiled + pos_repeated

def edges_line_index(graph):
    smoothness = circle_mesh.shape[0]
    pos = np.array(graph.get_edgelist(), dtype=np.ubyte).flatten()
    return pos * smoothness

def edges_line_array(graph):
    vertex_pos = np.array(graph.vs["pos"], dtype = np.float32)
    edges_index = np.array(graph.get_edgelist(), dtype=np.int).flatten()
    return np.take(vertex_pos, edges_index, 0)

def edges_triangle_mesh(graph, hw):
    linearray = edges_line_array(graph)
    offset = linearray[1::2] - linearray[0::2]
    offset_sized = hw*linalg.norm(offset)
    array = np.empty((linearray*2,2), dtype=float32)
    arrar[0::2] = linearray - offset_sized
    arrar[1::2] = linearray + offset_sized
    ## create index array (0,1,2,3,1,2,4,5,6,7,4,5)
    index = np.repeat(np.arange(0, linearray.shape[0]*3/2, dtype=ubyte),2)
    index[3::6] = index[3::6] + 4

def circle_mesh(smoothness):
    return Mesh(circle_array(smoothness), circle_index(smoothness))

def circle_array(smoothness):
    #make an array with transformation vectors
    #for n equidistant angles around the unit circle
    angles = np.linspace(0, 2*np.pi, smoothness, True, dtype=np.float32)
    c = np.cos(angles)
    s = np.sin(angles)
    npoints = angles.shape[0]
    rotations = np.zeros((npoints,2), dtype=np.float32)
    rotations[:,0] = c
    rotations[:,1] = s
    rotations[0,:] = 0
    return rotations

def circle_index(smoothness):
    #make an index array with middle, angle1, angle2, middle, angle2..
    #so it can be passed as a triangle array
    index = np.empty((smoothness-1)*3, dtype=ubyte)
    index[0::3] = np.zeros(smoothness-1, dtype=ubyte)
    index[1::3] = np.arange(1, smoothness, dtype=ubyte)
    index[2::3] = np.arange(2, smoothness + 1, dtype=ubyte)
    return index
