from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import sys 

from Block import Block
from Optimizer import Optimizer
from Sheet import Sheet


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, blocks):
        super().__init__()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.exportButton = QtWidgets.QPushButton()
        self.importButton = QtWidgets.QPushButton()
        self.startButton = QtWidgets.QPushButton()

        self.exportButton.setText("Export")
        self.importButton.setText("Import")
        self.startButton.setText("Start")

        self.horizontalLayout.addWidget(self.exportButton)
        self.horizontalLayout.addWidget(self.importButton)
        self.horizontalLayout.addWidget(self.startButton)

        self.exportButton.clicked.connect()
        self.importButton.clicked.connect()
        self.startButton.clicked.connect()


        self.blocks = blocks
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def importBlocks(self):
        pass

    def exportBlocks(self):
        pass

    def startOpt(self):
        pass


    def draw_something(self):
        painter = QtGui.QPainter(self.label.pixmap())
        # pen = QtGui.QPen()
        # pen.setWidth(1)
        # pen.setColor(QtGui.QColor('red'))
        # painter.setPen(pen)
        for block in self.blocks:
            painter.drawRect(*block.pos,block.width, block.height)
        painter.end()


if __name__ == "__main__":
    blocks = [Block(0, [0,0], 30, 30),Block(1, [0,0], 50, 30),Block(2, [0,0], 30, 50)]
    # app = QtWidgets.QApplication(sys.argv)
    # window = MainWindow(blocks)
    # window.show()
    # app.exec()
    sheet = Sheet(10,10)
    
    opt = Optimizer(1000, 100, 0.01, 0.8, 15, blocks, sheet)
    opt.start()