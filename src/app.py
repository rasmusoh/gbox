from PyQt4 import QtGui, QtCore
import sys
from widgets import QtCode, plotwidget
import sourceutil
import igraph
import numpy.random as rdn
import mesh

class ModeSelector(QtGui.QWidget):
    def __init__(self):
        super(ModeSelector, self).__init__()

class SideBarWidget(QtGui.QWidget):
    width = 400;
    def __init__(self, parent, graph, redraw):
        super(SideBarWidget, self).__init__(parent)
        self.modeselector = ModeSelector()
        self.codewidget = QtCode.QAlgorithmWidget(self, graph, redraw)
        self.codewidget.importfunctions(self.importtstatic(), self.importtstart(), self.importtstep())

    def importtstatic(self):
        import algorithms.statics
        return sourceutil.func_bodies_from_module(algorithms.statics)

    def importtstart(self):
        import algorithms.starts
        return sourceutil.func_bodies_from_module(algorithms.starts)

    def importtstep(self):
        import algorithms.steps
        return sourceutil.func_bodies_from_module(algorithms.steps)

    def addmodes(self):
        modes = {
                "MOVE":     QtGui.QIcon("../icons/move-small.gif"),
                "ADD" :     QtGui.QIcon("../icons/add-small.gif"),
                "CONNECT":  QtGui.QIcon("../icons/connect-small.gif"),
                "ERASE":    QtGui.QIcon("../icons/erase-small.gif"),
                "BA":       QtGui.QIcon("../icons/ba-small.gif"),
                "TREE":     QtGui.QIcon("../icons/tree-small.gif"),
                "NEIGHBOUR":QtGui.QIcon("../icons/neighbour-small.gif"),
                "PLAY":     QtGui.QIcon("../icons/play-small.gif"),
                "PAUSE":    QtGui.QIcon("../icons/pause-small.gif")
                }

# self.setGeometry(800, 0, 400, 800)
##self.setGeometry(800, 0, self.widget.width, self.widget.height)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = MainWidget(self)
        self.setGeometry(800, 0, self.widget.width, self.widget.height)
        self.setCentralWidget(self.widget)
        self.show()

class MainWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        graph = self.testgraph()
        self.plot = plotwidget.PlotWidget()
        self.plot.mesh = mesh.NetworkThickMesh(25, 0.002, graph)
        self.sidebar = SideBarWidget(self, graph, self.redraw)
        self.layout = QtGui.QGridLayout(self)
        self.layout.addWidget(self.plot, 0,0)
        self.layout.addWidget(self.sidebar, 0,1)
        self.layout.setColumnStretch(0,3);
        self.layout.setColumnStretch(1,1);
        self.setLayout(self.layout)

        self.width, self.height = self.plot.width + self.sidebar.width, self.plot.height

    def testgraph(self):
        g = igraph.Graph.Full(100)
        g.vs["pos"] = 0.4*rdn.randn(100,2)
        g.vs["size"] = 0.02*rdn.randn(100,1) + 0.05
        return g

    def redraw(self):
        print "redraw"
        self.plot.meshChanged()

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
