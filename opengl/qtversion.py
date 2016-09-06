# PyQt4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
import tree

class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 1000, 800

    def set_data(self, data):
        """Load 2D data as a Nx2 Numpy array.
        """
        self.data = data
        self.count = data.shape[0]

    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)
        # create a Vertex Buffer Object with the specified data
        self.vbo = glvbo.VBO(self.data)

    def update_data(self, data):
        self.vbo.set_array(data)
        self.count = data.shape[0]
        self.update()

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set yellow color for subsequent drawing rendering calls
        gl.glColor(1,1,0)
        # bind the VBO
        self.vbo.bind()
        # tell OpenGL that the VBO contains an array of vertices
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        # these vertices contain 2 single precision coordinates
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.vbo)
        # draw "count" points from the VBO
        gl.glDrawArrays(gl.GL_LINES, 0, self.count)

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
        ar = width / float(height)
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(-1 * ar, 1 * ar, 1, -1, -1, 1)

if __name__ == '__main__':
    # import numpy for generating random data points
    import sys
    import numpy as np
    import numpy.random as rdn
    import re

    # define a Qt window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            self.widget = MainWidget(self)
            # put the window at the screen position (100, 100)
            self.setGeometry(800, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

    class MainWidget(QtGui.QWidget):

        def __init__(self, parent):        
            
            super(MainWidget, self).__init__(parent)
            self.data = tree.Tree(np.array([0,1], dtype=np.float32), -0.3, np.pi/2,  12).get_lines_np()

            # generate random data points
            ##self.data = np.array(.2*rdn.randn(100000,2),dtype=np.float32)
            ##self.data = np.array([[0.1,0.2],[0.1,0.2]] ,dtype=np.float32)

            # initialize the GL widget
            self.plot = GLPlotWidget()
            self.plot.set_data(self.data)
            self.layout = QtGui.QGridLayout(self)
            self.layout.addWidget(self.plot, 0,0)
            self.layout.addWidget(SideBarWidget(self), 0,1)
            self.layout.setColumnStretch(0,1)
            self.setLayout(self.layout)

            self.width, self.height = self.plot.width, self.plot.height

        def redrawTree(self, data):
            self.data = data
            self.plot.update_data(self.data)

    class SideBarWidget(QtGui.QWidget):
        def __init__(self, parent):        
            
            super(SideBarWidget, self).__init__(parent)
            self.layout = QtGui.QVBoxLayout(self)

            self.entry = MyQTextEdit()
            self.entry.textChanged.connect(self.changed)
            self.entry.setText("tree.Tree(np.array([0,1], dtype=np.float32), -0.3, np.pi/2,  12)")
            self.layout.addWidget(self.entry)

            self.button1 = QtGui.QPushButton("Eval")
            self.button1.clicked.connect(self.b1clicked)
            self.layout.addWidget(self.button1)
           
            self.setLayout(self.layout)

        def changed(self):
            try:
                code = unicode(self.entry.toPlainText().toUtf8(), encoding="UTF-8")
                tree = eval(code)
                self.parentWidget().redrawTree(tree.get_lines_np())
            except:
                pass

        def b1clicked(self):
            self.tryinc()

    class MyQTextEdit(QtGui.QTextEdit):
        ctrlHeldDown = False
        shiftHeldDown = False

        def keyPressEvent(self, e):
            if e.key() == QtCore.Qt.Key_Control:
                self.ctrlHeldDown = True 
            if e.key() == QtCore.Qt.Key_Shift:
                self.shiftHeldDown = True
            if self.ctrlHeldDown and e.key() == QtCore.Qt.Key_Up:
                self.tryinc()
            if self.ctrlHeldDown and e.key() == QtCore.Qt.Key_Down:
                self.trydec()
            else:
                super(MyQTextEdit, self).keyPressEvent(e)

        def keyReleaseEvent(self, e):
            if e.key() == QtCore.Qt.Key_Control:
                self.ctrlHeldDown = False
            elif e.key() == QtCore.Qt.Key_Shift:
                self.shiftHeldDown = False
            super(MyQTextEdit, self).keyPressEvent(e)

        def tryinc(self):
            if self.shiftHeldDown:
                self.tryadd(0.01)
            else:
                self.tryadd(1)

        def trydec(self):
            if self.shiftHeldDown:
                self.tryadd(-0.01)
            else:
                self.tryadd(-1)

        def tryadd(self, amount):
            entry = self.toPlainText()
            pos =  self.textCursor().position()
            for m in re.finditer(r"-?[0-9]+\.?[0-9]*", entry):
                if m.start() <= pos and m.end() >= pos:
                    num = m.group(0)
                    incednum = float(num) + amount
                    modentry = entry[:m.start()] + str(incednum) + entry[m.end():]
                    self.setText(modentry)
                    cursor = self.textCursor()
                    cursor.setPosition(m.start()+1)
                    self.setTextCursor(cursor)

    # create the Qt App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
app.exec_()
