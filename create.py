from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
import os

class CreateWindow(QWidget):
    created = pyqtSignal()
    
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.destionaryPath = None
        self.newFolders = []
        self.newFiles = []
        self.setupUi()
        
        self.selectPath.clicked.connect(self.selectDirectory)
        self.add.clicked.connect(self.addItem)
        self.remove.clicked.connect(self.removeItem)
        self.create_.clicked.connect(self.createFunc)
        self.cancel.clicked.connect(self.closeWidget)
        
    def setupUi(self):
        self.setWindowIcon(QtGui.QIcon('./pictures/addFol.png'))
        self.setWindowTitle(f"Create new {self.type}")
        self.setFixedSize(270, 400)
        self.layout_ = QVBoxLayout()
        self.selectPath = QPushButton("Select Path", self)
        self.layout_.addWidget(self.selectPath)
        self.path = QLineEdit(self)
        self.path.setReadOnly(True)
        self.path.setPlaceholderText("Path to save")
        self.layout_.addWidget(self.path)
        self.label = QLabel(f"List {self.type}:",self)
        self.layout_.addWidget(self.label)
        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.layout_.addWidget(self.listWidget)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText(f"Name {self.type}")
        self.layout_.addWidget(self.lineEdit)
        self.add = QPushButton("Add", self)
        self.layout_.addWidget(self.add)
        self.remove = QPushButton("Remove", self)
        self.layout_.addWidget(self.remove)
        self.create_ = QPushButton("Create", self)
        self.layout_.addWidget(self.create_)
        self.cancel = QPushButton("Cancel", self)
        self.layout_.addWidget(self.cancel)
        self.setLayout(self.layout_)
    
    def selectDirectory(self):
        root_directory = "./root"
        self.destionaryPath = QFileDialog.getExistingDirectory(self, "Select directory to save", root_directory)
        self.path.setText(self.destionaryPath)
          
    def addItem(self):
        item = QListWidgetItem(self.lineEdit.text())
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.lineEdit.clear()
    
    def removeItem(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))
 
    def createFunc(self):
        if self.destionaryPath is None:
            QMessageBox.warning(self, "Warning!", "Please select a directory to save!")
            return
        if self.listWidget.count() == 0:
            QMessageBox.warning(self, "Warning!", "List is empty!")
            return
        self.newItems = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        if not self.newItems:
            QMessageBox.warning(self, "Warning", "List is empty!")
        else:
            try:
                if self.type == "folders":
                    for folder in self.newItems:
                        folderPath = os.path.join(self.destionaryPath, folder).replace("\\", "/")
                        self.newFolders.append(folderPath)
                        os.makedirs(folderPath)
                else:
                    for file in self.newItems:
                        filePath = os.path.join(self.destionaryPath, file).replace("\\", "/")
                        self.newFiles.append(filePath)
                        with open(filePath, "w") as f:
                            f.write("")
                QMessageBox.information(self, "Success!", f"Created {self.type} successfully!")
                self.created.emit()
                self.closeWidget()
            except Exception as e:
                QMessageBox.critical(self, f"Created {self.type} error!", f"{e}")
    
    def closeWidget(self):
        self.close()
