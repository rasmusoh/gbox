from PyQt4 import QtGui, QtCore
import re
import sys

class QAlgorithmWidget(QtGui.QWidget):
    def __init__(self, parent, data, redraw):
        
        super(QAlgorithmWidget, self).__init__(parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.redraw = redraw
        self.data = data

        self.staticedit = QFunctionWidget("def static(graph):")
        self.staticedit.funchanged.connect(self.staticchanged)
        self.layout.addWidget(self.staticedit)

        self.startedit = QFunctionWidget("def onstart(graph, **kwargs):")
        self.startedit.funchanged.connect(self.startchanged)
        self.layout.addWidget(self.startedit)

        self.stepedit = QFunctionWidget("def onstep(graph):")
        self.stepedit.funchanged.connect(self.stepchanged)
        self.layout.addWidget(self.stepedit)

        self.button1 = QtGui.QPushButton("Run")
        self.button1.clicked.connect(self.startstop)
        self.layout.addWidget(self.button1)

        self.onstart = self.startedit.getfunction()
        self.onstep = self.stepedit.getfunction()
        self.static = self.staticedit.getfunction()

        self.running = False
        self.live = True
        self.screenw = 800
        self.screenh = 800
       
        self.setLayout(self.layout)

    def importfunctions(self, statics, starts, steps):
        self.staticedit.setfunctions(statics)
        self.startedit.setfunctions(starts)
        self.stepedit.setfunctions(steps)

    def startstop(self):
        if self.running:
            self.stop()
        else:
            self.run()

    def stop(self):
        self.running = False

    def run(self):
        self.onstart(self.data, w = self.screenw, h=self.screenh)
        self.running = True
        self.live = True

    def update(self):
        if self.running:
            self.onstep(self.data)
            self.redraw()

    def staticchanged(self):
        self.static = self.staticedit.getfunction()
        if self.live:
            self.static(self.data)
            self.redraw()

    def startchanged(self):
        self.onstart = self.startedit.getfunction()

    def stepchanged(self):
        self.onstep = self.stepedit.getfunction()

class QFunctionWidget(QtGui.QWidget):
    funchanged = QtCore.pyqtSignal()

    def __init__(self, funheader):        
        super(QFunctionWidget, self).__init__()
        self.function = None
        self.functions = {"": "pass"}
        self.lastworkingsource = "pass"
        self.error = ""
        self.compilefunheader =  re.sub(r'^def \w+',"def fun",funheader) #change the name internally to 'fun' 
                                                                         #so we know the name when calling exec()
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addStretch(1)

        self.selector = QtGui.QComboBox()
        self.selector.setEditable(False)
        self.selector.currentIndexChanged.connect(self.changefunction)
        self.layout.addWidget(self.selector)

        self.label = QtGui.QLabel()
        self.label.setText(funheader)
        self.layout.addWidget(self.label)

        self.editor = QFunctionEdit(funheader)
        self.editor.textChanged.connect(self.updatefunction)
        self.layout.addStretch(1)
        self.layout.addWidget(self.editor)

        self.setLayout(self.layout)

    def setfunctions(self, functions):
        self.functions = functions
        self.selector.addItems(self.functions.keys())
        self.changefunction()

    def updatefunction(self):
        try:
            self.function = self.compilefunction()
            self.funchanged.emit()
            self.lastworkingsource = self.editor.toPlainText()
        except Exception as e:
            self.error = e
            print self.error, self.error.args

    def changefunction(self):
        if self.selector.currentText() in self.functions.keys():
            funkey = qstring_to_unicode(self.selector.currentText())
            self.editor.setText(self.functions[funkey])

    def compilefunction(self):
        functionsource = self.compilefunheader+"\n" +self.editor.getunicode()
        exec(functionsource)
        return fun

    def getfunction(self):
        return self.function
        
    def reverttoworking(self):
        self.editor.setText(self.lastworkingsource)

class QFunctionEdit(QtGui.QTextEdit):
    ctrlHeldDown = False
    shiftHeldDown = False
    delta = 1
    smalldelta = 0.01

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
            super(QFunctionEdit, self).keyPressEvent(e)

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_Control:
            self.ctrlHeldDown = False
        elif e.key() == QtCore.Qt.Key_Shift:
            self.shiftHeldDown = False
        super(QFunctionEdit, self).keyPressEvent(e)

    def tryinc(self):
        if self.shiftHeldDown:
            self.tryadd(self.smalldelta)
        else:
            self.tryadd(self.delta)

    def trydec(self):
        if self.shiftHeldDown:
            self.tryadd(-self.smalldelta)
        else:
            self.tryadd(-self.delta)

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

    def getunicode(self):
        return qstring_to_unicode(self.toPlainText())


def qstring_to_unicode(qstring):
    return unicode(qstring.toUtf8(), encoding="UTF-8")
