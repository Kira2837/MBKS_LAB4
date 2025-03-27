from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
import os
import shutil
 
class DeleteWindow(QWidget):
    deleted = pyqtSignal()
    
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.folderPaths = []
        self.filePaths = []
        self.deletedSubFolders = []
        self.deletedFilesInFolders = []
        self.setupUi()
        
        self.selectPath.clicked.connect(self.selectDirectory)
        self.add.clicked.connect(self.addItem)
        self.remove.clicked.connect(self.removeItem)
        self.delete.clicked.connect(self.deleteFunc)
        self.cancel.clicked.connect(self.closeWidget)
        
    def setupUi(self):
        self.setWindowIcon(QtGui.QIcon('./pictures/deleteFol.png'))
        self.setWindowTitle(f"Delete {self.type}")
        self.setFixedSize(270, 400)
        self.layout_ = QVBoxLayout()
        self.selectPath = QPushButton("Select Path", self)
        self.layout_.addWidget(self.selectPath)
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
        self.delete = QPushButton("Delete", self)
        self.layout_.addWidget(self.delete)
        self.cancel = QPushButton("Cancel", self)
        self.layout_.addWidget(self.cancel)
        self.setLayout(self.layout_)

    def selectDirectory(self):
        root_directory = "./root"
        if self.type == "folders":
            # absolute path
            folderPath = QFileDialog.getExistingDirectory(self, "Select folder to delete", root_directory)
            if not folderPath:
                return
            self.folderPaths.append(folderPath)
            self.lineEdit.setText(folderPath)
        elif self.type == "files":
            # absolute path
            filePath, _ = QFileDialog.getOpenFileName(self, "Select file to delete", root_directory)
            if not filePath:
                return 
            self.filePaths.append(filePath)
            self.lineEdit.setText(filePath)
        
          
    def addItem(self):
        item = QListWidgetItem(self.lineEdit.text())
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.lineEdit.clear()
    
    def removeItem(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))
    
    def deleteFunc(self):
        if self.listWidget.count() == 0:
            QMessageBox.warning(self, "Warning!", f"Please add {self.type} to delete!")
            return
        if self.type == "folders":
            for folderPath in self.folderPaths:
                try:
                    for dirpath, dirs, files in os.walk(folderPath):
                        if dirpath != folderPath:
                            self.deletedSubFolders.append(dirpath.replace("\\", "/"))
                        self.deletedFilesInFolders.extend([os.path.join(dirpath, file).replace("\\", "/") for file in files])
                    shutil.rmtree(folderPath)
                except Exception as e:
                    QMessageBox.critical(self, "Delete folder error!", f"{e}")
            self.folderPaths.extend(self.deletedSubFolders)
        elif self.type == "files":
            for filePath in self.filePaths:
                try:
                    os.remove(filePath)
                except Exception as e:
                    QMessageBox.critical(self, "Delete file error!", f"{e}")
        QMessageBox.information(self, "Success!", f"Deleted {self.type} successfully!")
        self.deleted.emit()
        self.closeWidget()
    
    def closeWidget(self):
        self.close()