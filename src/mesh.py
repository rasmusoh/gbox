import numpy as np
import numpy.linalg as linalg
import igraph
import OpenGL.GL as gl

class Mesh:
    def __init__(self, array, index):
        self.array = array
        self.index = index
        self.triangle_size = index.shape[0]
        self.line_size = 0
        self.line_start = 0
        self.array_type = gl.GL_FLOAT
        self.index_type = gl.GL_UNSIGNED_INT

    def combine(self, b):
        array = np.concatenate((self.array, b.array))
        index = np.concatenate((self.index, self.array.shape[0] + b.index))
        self.triangle_size = index.shape[0]
        return Mesh(array, index)

    def add_lines(self, lines_index):
        if self.line_size == 0:
            self.line_start = self.index.shape[0]
        self.line_start = self.line_start + lines_index.shape[0]
        self.index = np.concatenate((self.index, lines_index))

class NetworkLineMesh:
    def __init__(self, smoothness, graph):
        self.circle_mesh = circle_mesh(smoothness)
        self.update_mesh(graph)

    def update_mesh(self, graph):
        self.mesh = verteces_mesh(graph, self.circle_mesh).add_lines(edges_line_index(graph, self.circle_mesh))

    def get_mesh(self):
        return self.mesh

class NetworkThickMesh:
    def __init__(self, smoothness, width, graph):
        self.hw = width/2
        self.circle_mesh = circle_mesh(smoothness)
        self.update_mesh(graph)

    def update_mesh(self, graph):
        vmesh = verteces_mesh(graph, self.circle_mesh)
        emesh = edges_triangle_mesh(graph, self.hw)
        self.mesh = vmesh.combine(emesh)

    def get_mesh(self):
        return self.mesh

def verteces_mesh(graph, circle_mesh):
    return Mesh(verteces_array(graph, circle_mesh), verteces_index(graph, circle_mesh))

def verteces_array(graph, circle_mesh):
    positions = np.array(graph.vs["pos"], dtype = np.float32)
    sizes = np.array(graph.vs["size"], dtype = np.float32)
    ncircles = positions.shape[0]
    smoothness = circle_mesh.array.shape[0]

    pos_repeated = np.repeat(positions, smoothness, 0)
    size_repeated = np.repeat(sizes, smoothness)
    circle_tiled = np.tile(circle_mesh.array, (ncircles,1)).T

    return pos_repeated + (circle_tiled * size_repeated).T

def verteces_index(graph, circle_mesh):
    ncircles = len(graph.vs)
    points_per_circle = circle_mesh.array.shape[0]
    indeces_per_circle = circle_mesh.index.shape[0]
    pos = np.arange(0, ncircles*points_per_circle, points_per_circle, dtype=np.uint32)

    circle_tiled = np.tile(circle_mesh.index, ncircles)
    pos_repeated =np.repeat(pos, indeces_per_circle)

    return circle_tiled + pos_repeated

def edges_line_index(graph):
    smoothness = circle_mesh.shape[0]
    pos = np.array(graph.get_edgelist(), dtype=np.uint32).flatten()
    return pos * smoothness

def edges_line_array(graph):
    vertex_pos = np.array(graph.vs["pos"], dtype = np.float32)
    edges_index = np.array(graph.get_edgelist(), dtype=np.int).flatten()
    return np.take(vertex_pos, edges_index, 0)

def edges_triangle_mesh(graph, hw):
    linearray = edges_line_array(graph)
    offset = edges_line_offsets(linearray, hw)
    array = np.empty((linearray.shape[0]*2,2), dtype=np.float32)
    array[0::2] = linearray - offset
    array[1::2] = linearray + offset
    return Mesh(array, edges_triangle_index(linearray))

def edges_triangle_index(linearray):
    nrectangles = linearray.shape[0]/2
    points_per_rectangle = 4
    indeces_per_rectangle = 6

    pos = np.arange(0, nrectangles*points_per_rectangle, points_per_rectangle, dtype=np.uint32)
    rectangle_tiled = np.tile(rectangle_index_array, nrectangles)
    pos_repeated = np.repeat(pos, indeces_per_rectangle)
    return  rectangle_tiled + pos_repeated

def edges_line_offsets(linearray, hw):
    parallel = linearray[0::2] -linearray[1::2]
    offset = np.empty_like(parallel)
    offset[:,0] = -parallel[:,1]
    offset[:,1] = parallel[:,0]
    offset_norms = np.apply_along_axis(linalg.norm, 1, offset)
    offset_sized = hw * offset / offset_norms[:, np.newaxis]
    offset_repeated = np.repeat(offset_sized,2, 0)
    return offset_repeated

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
    index = np.empty((smoothness-1)*3, dtype=np.uint32)
    index[0::3] = np.zeros(smoothness-1, dtype=np.uint32)
    index[1::3] = np.arange(1, smoothness, dtype=np.uint32)
    index[2::3] = np.arange(2, smoothness + 1, dtype=np.uint32)
    index[-1] = 1
    return index

rectangle_index_array = np.array([0,1,2,1,2,3], dtype=np.uint32)
