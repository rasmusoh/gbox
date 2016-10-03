import sys
import numpy.random as rdn
import numpy as np
import igraph
import glnetworkplotwidget as npw
import mesh
from PyQt4 import QtGui

class TestWindow(QtGui.QMainWindow):
    def __init__(self):
        super(TestWindow, self).__init__()
        self.widget = npw.GLNetworkPlotWidget(self)

        graph = self.testgraph()
        self.widget.mesh = mesh.NetworkThickMesh(25, 0.2, graph)
        self.setGeometry(800, 0, self.widget.width, self.widget.height)
        self.setCentralWidget(self.widget)
        self.show()

    def testgraph(self):
        # g = igraph.Graph.Full(10)
        # g.vs["pos"] = 0.4*rdn.randn(100,2)
        # g.vs["size"] = 0.02*rdn.randn(100,1) + 0.05
        g = igraph.Graph.Full(2)
        g.vs["pos"] = np.array([[0.5, 0.5], [ -0.5, -0.5]], dtype=np.float32)
        g.vs["size"] = 0.02*rdn.randn(2,1) + 0.05
        return g

def run():
    # create the Qt App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    run()
