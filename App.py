from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import sys 
import numpy as np
import pandas as pd

from Block import Block
from Optimizer import Optimizer
from Sheet import Sheet


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, blocks):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setWindowTitle("VLSI Optimizer")
        # self.setWindowIcon(QtGui.QIcon('App/data/images/icon.png'))
        self.setCentralWidget(self._main)

        self.layout = QtWidgets.QVBoxLayout(self._main)

        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.exportButton = QtWidgets.QPushButton()
        self.importButton = QtWidgets.QPushButton()
        self.startButton = QtWidgets.QPushButton()

        self.exportButton.setText("Export")
        self.importButton.setText("Import")
        self.startButton.setText("Start")

        self.buttonsLayout.addWidget(self.importButton)
        self.buttonsLayout.addWidget(self.exportButton)
        self.buttonsLayout.addWidget(self.startButton)

        self.importButton.clicked.connect(self.importBlocks)       
        self.exportButton.clicked.connect(self.exportBlocks)
        self.startButton.clicked.connect(self.startOptimization)

        self.inputLayout = QtWidgets.QHBoxLayout()
        self.paneWidthInput = QtWidgets.QLineEdit()
        self.paneHeightInput = QtWidgets.QLineEdit()
        self.populationSizeInput = QtWidgets.QLineEdit()
        self.epochNumberInput = QtWidgets.QLineEdit()

        self.paneWidthInput.setValidator(QtGui.QIntValidator())
        self.paneHeightInput.setValidator(QtGui.QIntValidator())
        self.populationSizeInput.setValidator(QtGui.QIntValidator())
        self.epochNumberInput.setValidator(QtGui.QIntValidator())

        self.paneWidthInput.setPlaceholderText("Pane width")
        self.paneHeightInput.setPlaceholderText("Pane height")
        self.populationSizeInput.setPlaceholderText("Population size")
        self.epochNumberInput.setPlaceholderText("Number of epochs")

        self.inputLayout.addWidget(self.paneWidthInput)
        self.inputLayout.addWidget(self.paneHeightInput)
        self.inputLayout.addWidget(self.populationSizeInput)
        self.inputLayout.addWidget(self.epochNumberInput)
        
        self.layout.addLayout(self.inputLayout)
        self.layout.addLayout(self.buttonsLayout)

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(5*260, 5*260)
        canvas.fill(QtGui.QColor(255,255,255))
        self.label.setPixmap(canvas)
        self.layout.addWidget(self.label)
        
        self.finalSolution = None
        self.blocks = None
        self.genAlg = None


    def importBlocks(self):
        canvas = QtGui.QPixmap(5*260, 5*260)
        canvas.fill(QtGui.QColor(255,255,255))
        self.label.setPixmap(canvas)
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file to import...',filter='*.xlsx')
        if file_name == '': 
            return
        self._importBlocks(file_name)
        
    def _importBlocks(self, path):
        df = pd.read_excel(path[0], header=0)
        self.blocks = []
        for index, row in df.iterrows():
            self.blocks.append(Block(index, [0, 0], row["Width"], row["Height"]))
        self.drawBlocks()

    def exportBlocks(self):
        file_path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file_path == '': 
            return
        file_path += "/results.xlsx"
        self._exportBlocks(file_path)
        

    def _exportBlocks(self, path):
        if self.finalSolution is None:
            return
        blocksDic = {
            'id': [block.id for block in self.finalSolution["blocksPosition"]],
            'width': [block.width for block in self.finalSolution["blocksPosition"]],
            'height': [block.height for block in self.finalSolution["blocksPosition"]],
            'posX': [block.pos[0] for block in self.finalSolution["blocksPosition"]],
            'posY': [block.pos[1] for block in self.finalSolution["blocksPosition"]],
        }
        df = pd.DataFrame(blocksDic)
        df.to_excel(path)

    def startOptimization(self):
        # Wyczyść tab 
        # Wyłącz przyciski
        # Start optymalizacji
        # Pokaż statusbar
        # Załaduj najlepszy wynik
        # Możliwość przeglądania wyników TODO dodać strzałki prawo lewo
        canvas = QtGui.QPixmap(5*260, 5*260)
        canvas.fill(QtGui.QColor(255,255,255))
        self.label.setPixmap(canvas)
        populationSize = int(self.populationSizeInput.text())
        epochs = int(self.epochNumberInput.text())
        populationSize = int(self.populationSizeInput.text())
        sheetW = int(self.paneWidthInput.text())
        sheetH = int(self.paneHeightInput.text())
        sheet = Sheet(sheetW, sheetH)
        self.genAlg = Optimizer(populationSize,epochs,0.05,0.96,epochs//7*3,self.blocks, sheet)
        self.genAlg.start()
        self.finalSolution = self.genAlg.bestFromPopulation[0]
        self.drawBlocks(True)


    def drawBlocks(self, final=False):
        if final:
            blocks = self.finalSolution["blocksPosition"]
        else:
            blocks = self.blocks

        painter = QtGui.QPainter() 
        painter.begin(self.label.pixmap())
        painter.setPen(Qt.black)
        for block in blocks:
            painter.drawRect(5*block.pos[0],5*block.pos[1],5*block.width, 5*block.height)
            painter.drawText(
                QtCore.QPoint(5*block.pos[0] + 5*block.width//2, 
                5*block.pos[1]+5*block.height//2), f"{block.id}")
        painter.setPen(Qt.red)
        painter.drawRect(0,0,200*5,200*5)
        painter.end()


if __name__ == "__main__":
    # np.random.seed(12345)
    blocks = [
        Block(0, [0,0], 40, 30),
        Block(1, [0,0], 10, 70),
        Block(2, [0,0], 25, 70),
        Block(3, [0,0], 40, 60),
        Block(4, [0,0], 80, 40),
        Block(5, [0,0], 45, 60),
        Block(6, [0,0], 35, 70),
        Block(7, [0,0], 30, 60),
        Block(8, [0,0], 120, 40),
        Block(9, [0,0], 25, 60),
        Block(10, [0,0], 80, 70),
        Block(11, [0,0], 60, 60),
        Block(12, [0,0], 50, 70),
        Block(13, [0,0], 75, 30),
        Block(14, [0,0], 85, 30)]
    # sheet = Sheet(300, 300)
    # opt = Optimizer(100, 200, 0.3, 0.9, 50, blocks, sheet)
    # opt.start()
    # for i in opt.bestFromPopulation[0]["blocksPosition"]:
        # print(i)
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)
    app = MainWindow(blocks)
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
    