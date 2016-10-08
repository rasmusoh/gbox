from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
import numpy as np

class PlotWidget(QGLWidget):
    # default window size
    width, height = 1000, 800
    mousepressed = False
    ar = width/float(height)
    draginfo = np.zeros([2,2],dtype =np.float32)
    vselected = []
    initialized = False

    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        self.setMouseTracking(True)
        # background color
        gl.glClearColor(0,0,0,0)
        self.arrayVbo = glvbo.VBO(self.mesh.array)
        self.indexVbo = glvbo.VBO(self.mesh.index, target=gl.GL_ELEMENT_ARRAY_BUFFER)
        self.initialized = True

    def meshChanged(self, mesh):
        self.mesh = mesh
        if not self.initialized: 
            return
        self.arrayVbo.set_array(mesh.array)
        self.indexVbo.set_array(mesh.index)
        self.update()

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glColor(1,1,0)
        self.arrayVbo.bind()
        self.indexVbo.bind()

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 2, self.mesh.array_type, gl.GL_FALSE, 0, None)
        gl.glDrawElements(gl.GL_TRIANGLES, self.mesh.triangle_size, self.mesh.index_type, None)

    def paintBox(self):
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
        bb = (min(self.draginfo[:,0]),
             max(self.draginfo[:,0]),
             min(self.draginfo[:,1]),
             max(self.draginfo[:,1]))
        self.vselected = {v for v in self.graph.vs if inboundingbox(v["pos"], bb)}

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
