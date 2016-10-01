from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
import rendergraph
import numpy as np

class GLGraphPlotWidget(QGLWidget):
    # default window size
    width, height = 1000, 800
    mousepressed = False
    ar = width/float(height)
    draginfo = np.zeros([2,2],dtype =np.float32)
    vselected = []

    def graph_to_vbo(self, graph):
        self.graph = graph
        self.smoothness = 24
        self.vs, self.index = rendergraph.array_verteces_graph(graph, self.smoothness)
        self.edgecount = self.es.shape[0]
        self.vertexcount = self.vs.shape[0]

    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        self.setMouseTracking(True)
        # background color
        gl.glClearColor(0,0,0,0)
        # create a Vertex Buffer Object with the specified data
        self.edgevbo = glvbo.VBO(self.es)
        self.vertexvbo = glvbo.VBO(self.vs)

    def update_data(self, graph):
        self.graph_to_vbo(graph)
        self.edgevbo.set_array(self.es)
        self.edgecount = self.es.shape[0]
        self.vertexvbo.set_array(self.vs)
        self.vertexcount = self.vs.shape[0]
        self.update()

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set yellow color for subsequent drawing rendering calls
        gl.glColor(1,1,0)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        self.paintVerteces()

    def paintVerteces(self):
        # bind the VBO
        self.vertexvbo.bind()
        # tell OpenGL that the VBO contains an array of vertices
        # these vertices contain 2 single precision coordinates
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.edgevbo)
        # draw "count" points from the VBO
        gl.glDrawArrays(gl.GL_LINES, 0, self.edgecount)

    def paintTriangles(self):
        # bind the VBO
        # tell OpenGL that the VBO contains an array of vertices
        # these vertices contain 2 single precision coordinates
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.vertexvbo)
        gl.glColorPointer(3, gl.GL_FLOAT,)
        # draw "count" points from the VBO
        for i in range(0, self.vertexcount):
            gl.glDrawArrays(gl.GL_TRIANGLE_FAN, i*self.smoothness,self.smoothness)

    def paintBox(self):
        # e = 0.05
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glColor(0,0,1)
        gl.glVertex2f(self.draginfo[0][0], self.draginfo[0][1])
        gl.glVertex2f(self.draginfo[1][0], self.draginfo[0][1])
        gl.glVertex2f(self.draginfo[1][0], self.draginfo[1][1])
        gl.glVertex2f(self.draginfo[0][0], self.draginfo[1][1])
        gl.glEnd()


    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, width, height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        self.ar = width / float(height)
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(-1 * self.ar, 1 * self.ar, 1, -1, -1, 1)

    def screentoworld(self, x, y):
        return self.ar*(2*x/float(self.width)-1), 2*y/float(self.height)-1

    def updateselected(self):
        bb = min(self.draginfo[:,0]),
             max(self.draginfo[:,0]),
             min(self.draginfo[:,1]),
             max(self.draginfo[:,1]),
        self.vselected = {v in self.graph.vs if inboundingbox(v["pos"], bb)}

    def mousePressEvent(self, e):
        self.mousepressed = True
        self.draginfo[:] =  self.screentoworld(e.x(), e.y())
        self.update()

    def mouseReleaseEvent(self, e):
        self.mousepressed = False
        self.draginfo[:,:] = 0
        self.update()

    def mouseMoveEvent(self, e):
        if self.mousepressed:
            self.draginfo[1] = self.screentoworld(e.x(), e.y())
            self.updateselected()
            self.update()

def inboudningbox(point, bb):
    return point >= bb[0] and point <= bb[1] and point >= bb[2] and point <= bb[3]

if __name__ == '__main__':
    # import numpy for generating random data points
    import sys
    import numpy as np
    import numpy.random as rdn
    import igraph
    import re

    # define a Qt window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            self.widget = GLGraphPlotWidget(self)

            self.widget.graph_to_vbo(self.testgraph())
            # put the window at the screen position (100, 100)
            self.setGeometry(800, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

        def testgraph(self):
            g = igraph.Graph.Full(10)
            g.vs["pos"] = 0.4*rdn.randn(100,2)
            g.vs["size"] = 0.02*rdn.randn(100,1) + 0.05
            return g


# create the Qt App and window
app = QtGui.QApplication(sys.argv)
window = TestWindow()
window.show()
app.exec_()
