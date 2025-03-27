from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
import os

class ChangeWindow(QWidget):
    changed = pyqtSignal()
    
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.folderPaths = []
        self.filePaths = []
        self.setupUi()
        
        self.selectPath.clicked.connect(self.selectDirectory)
        self.add.clicked.connect(self.addItem)
        self.remove.clicked.connect(self.removeItem)
        self.change.clicked.connect(self.changeFunc)
        self.cancel.clicked.connect(self.closeWidget)
        
    def setupUi(self):
        self.setWindowIcon(QtGui.QIcon('./pictures/changeFol.png'))
        self.setWindowTitle(f"Change {self.type}")
        self.setFixedSize(300, 400)
        self.layout_ = QVBoxLayout()
        self.selectPath = QPushButton("Select Path", self)
        self.layout_.addWidget(self.selectPath)
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Old Name", "New Name"])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout_.addWidget(self.tableWidget)
        
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText(f"Name {self.type}")
        self.layout_.addWidget(self.lineEdit)
        self.add = QPushButton("Add", self)
        self.layout_.addWidget(self.add)
        self.remove = QPushButton("Remove", self)
        self.layout_.addWidget(self.remove)
        self.change = QPushButton("Change", self)
        self.layout_.addWidget(self.change)
        self.cancel = QPushButton("Cancel", self)
        self.layout_.addWidget(self.cancel)
        self.setLayout(self.layout_)

    def selectDirectory(self):
        root_directory = "./root"
        if self.type == "folders":
            # absolute path
            folderPath = QFileDialog.getExistingDirectory(self, "Select folder to change", root_directory)
            if not folderPath:
                return
            self.folderPaths.append({folderPath: None})
            relative_path = os.path.relpath(folderPath).replace("\\", "/")
            self.lineEdit.setText(relative_path)
        elif self.type == "files":
            # absolute path
            filePath, _ = QFileDialog.getOpenFileName(self, "Select file to change", root_directory)
            if not filePath:
                return 
            self.filePaths.append({filePath: None})
            relative_path = os.path.relpath(filePath).replace("\\", "/")
            self.lineEdit.setText(relative_path)
        
          
    def addItem(self):
        if not self.lineEdit.text():
            return
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        item = QTableWidgetItem(self.lineEdit.text())
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setToolTip(self.lineEdit.text())
        self.tableWidget.setItem(rowPosition, 0, item) 
        fileName = self.lineEdit.text().split("/")[-1]
        item = QTableWidgetItem(self.lineEdit.text().replace(fileName, f"new_name_{self.type[:-1]}"))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setToolTip(item.text())
        self.tableWidget.setItem(rowPosition, 1, item)
        self.lineEdit.clear()
    
    def removeItem(self):
        selectedRows = sorted([item.row() for item in self.tableWidget.selectedItems()], reverse=True)
        for row in selectedRows:
            if self.type == "folders":
                folderPath = self.tableWidget.item(row, 0).text() 
                self.folderPaths.pop(row)
            elif self.type == "files":
                filePath = self.tableWidget.item(row, 0).text()
                self.filePaths.pop(row)
            self.tableWidget.removeRow(row)   
                
        self.tableWidget.clearSelection()
    
    def changeFunc(self):
        if self.tableWidget.rowCount() == 0:
            QMessageBox.warning(self, "Warning!", f"Please add {self.type} to change!")
            return
        for row in range(self.tableWidget.rowCount()):
            oldName = self.tableWidget.item(row, 0).text()
            newName = self.tableWidget.item(row, 1).text()
            if oldName == newName:
                continue
            try:
                if self.type == "folders":
                    os.rename(oldName, newName)
                    oldPath = list(self.folderPaths[row].keys())[0]
                    newPath = oldPath.replace(oldName, newName)
                    self.folderPaths[row][oldPath] = newPath
                elif self.type == "files":
                    os.rename(oldName, newName)
                    oldPath = list(self.filePaths[row].keys())[0]
                    newPath = oldPath.replace(oldName, newName)
                    self.filePaths[row][oldPath] = newPath
            except Exception:
                QMessageBox.critical(self, "Error!", f"Change {self.type} error!")
                return
        QMessageBox.information(self, "Success!", f"Changed {self.type} successfully!")
        self.changed.emit() 
        self.closeWidget()
    
    def closeWidget(self):
        self.close()