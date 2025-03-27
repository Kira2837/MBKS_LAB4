from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from UI import Ui_MainWindow
from create import CreateWindow
from change import ChangeWindow
from delete import DeleteWindow
import os
import shutil

NoneSecret = 0 
# 1-5
    
class DialogChange(QDialog):
    def __init__(self, title):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./pictures/level.png'))
        self.title = title
        self.newName = ''
        
        self.setFixedSize(250, 200)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        self.name_label = QtWidgets.QLabel()
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setPlaceholderText("New level")
        self.button_1 = QtWidgets.QPushButton("Submit")
        self.button_2 = QtWidgets.QPushButton("Cancel")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)
        
        self.button_1.clicked.connect(self.getNewName)
        self.button_2.clicked.connect(self.closeDiaglog)
    
    def getNewName(self):
        self.newName = self.name_edit.text()
        if (self.newName != ''):
            self.accept()
        else:
            QMessageBox.critical(self, "Error!", "Name cannot be empty!")
            
    def closeDiaglog(self):
        self.newName = ''
        self.accept()   


class mainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./pictures/magamentApp.png'))
        self.setWindowTitle("App management security")
        self.listWidget.setWordWrap(True)
        self.createWindow = None
        self.changeWindow = None
        self.deleteWindow = None
        
        self.rootDir = "./root"
        self.listDir = {}
        self.get_all_subdirectories(self.rootDir)
        self.setListSourceFolders()

        self.create.clicked.connect(self.createFolderOrFile)
        self.change.clicked.connect(self.changeFolderOrFile)
        self.delete_.clicked.connect(self.deleteFolderOrFile)
        self.select.clicked.connect(self.chooseFolder)
        self.submit.clicked.connect(self.changeLevelSecret)
        self.copy.clicked.connect(self.copy_file_securely)
        self.addLevel.clicked.connect(self.addLvl)
        self.deleteLevel.clicked.connect(self.delLvl)
        self.renameLevel.clicked.connect(self.renameLvl)
    
    def get_all_subdirectories(self, directory):
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                absPath = os.path.abspath(root).replace("\\", "/")
                self.listDir[os.path.join(absPath, dir).replace("\\", "/")] = 0
        self.listDir[os.path.abspath(self.rootDir).replace("\\", "/")] = 0
    
    def chooseFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select folder", self.rootDir)
        if not folderPath:
            return
        self.path.setPlainText(folderPath)
        value = self.listDir.get(folderPath)
        if value is None:
            return
        self.level.setCurrentIndex(value)
        
    def changeLevelSecret(self):
        folderPath = self.path.toPlainText()
        if folderPath == "":
            QMessageBox.warning(self, "Warning!", "Please select folder!")
            return
        
        parent_Dir = os.path.dirname(folderPath)
        level_parent = self.listDir.get(parent_Dir)
        level_child = self.level.currentIndex()
        if level_child < level_parent:
            QMessageBox.critical(self, "Error!", f"The secret level of the subfolder\n must be greater than or equal to\n the parent folder {parent_Dir}!")
            return
        self.listDir[folderPath] = level_child
        
        self.path.clear()
        for pathSubFolder, level in self.listDir.items():
                if os.path.commonpath([folderPath]) == os.path.commonpath([folderPath, pathSubFolder]) and level <= level_child:
                    self.listDir[pathSubFolder] = self.listDir[folderPath] 
                    item = QListWidgetItem(f"Changed the secret level of the folder {pathSubFolder}")
                    self.listWidget.addItem(item)
        QMessageBox.information(self, "Success!", "Change level secret successfully!")
        self.setListSourceFolders()
        
    def createFolderOrFile(self):   
        if (self.folders.isChecked()):
            self.createWindow = CreateWindow("folders")
        elif (self.files.isChecked()):
            self.createWindow = CreateWindow("files")
        else:
            return
        self.createWindow.show()
        self.createWindow.created.connect(lambda: self.infoCreatedFolders(self.createWindow.newFolders))
        self.createWindow.created.connect(lambda: self.infoCreatedFiles(self.createWindow.newFiles))
    
    def infoCreatedFolders(self, newFolders):
        if not newFolders:
            return
        for folder in newFolders:
            self.listDir[folder] = NoneSecret
            item = QListWidgetItem(f"Created folder {folder}")
            self.listWidget.addItem(item)
        self.setListSourceFolders()
    
    def infoCreatedFiles(self, newFiles):
        if not newFiles:
            return
        for file in newFiles:
            item = QListWidgetItem(f"Created file {file}")
            self.listWidget.addItem(item)
            
    def changeFolderOrFile(self):
        if (self.folders.isChecked()):
            self.changeWindow = ChangeWindow("folders")
        elif (self.files.isChecked()):
            self.changeWindow = ChangeWindow("files")
        else:
            return
        self.changeWindow.show()
        self.changeWindow.changed.connect(lambda: self.infoChangedFolders(self.changeWindow.folderPaths))
        self.changeWindow.changed.connect(lambda: self.infoChangedFiles(self.changeWindow.filePaths))
    
    def infoChangedFolders(self, folderPaths):
        if not folderPaths:
            return
        for folderPath in folderPaths:
            oldPathName = list(folderPath.keys())[0]
            newPathName = folderPath[oldPathName]
            level = self.listDir[oldPathName]
            self.listDir.pop(oldPathName)
            self.listDir[newPathName] = level
            
            item = QListWidgetItem(f"Changed name folder {oldPathName}. New name: {newPathName}")
            self.listWidget.addItem(item)
            self.setListSourceFolders()
    
    def infoChangedFiles(self, filePaths):
        if not filePaths:
            return
        for filePath in filePaths:
            oldPathName = list(filePath.keys())[0]
            newPathName = filePath[oldPathName]
            
            item = QListWidgetItem(f"Changed name file {oldPathName}. New name: {newPathName}")
            self.listWidget.addItem(item)
    
    def deleteFolderOrFile(self):  
        if (self.folders.isChecked()):
            self.deleteWindow = DeleteWindow("folders")
        elif (self.files.isChecked()):
            self.deleteWindow = DeleteWindow("files")
        else:
            return
        self.deleteWindow.show()
        self.deleteWindow.deleted.connect(lambda: self.infoDeletedFolders(self.deleteWindow.folderPaths, 
                                                                          self.deleteWindow.deletedFilesInFolders))
        self.deleteWindow.deleted.connect(lambda: self.infoDeletedFiles(self.deleteWindow.filePaths))
    
    def infoDeletedFolders(self, folderPaths, fileInFolders):
        if not folderPaths:
            return
        for folderPath in folderPaths:
            self.listDir.pop(folderPath)
            item = QListWidgetItem(f"Deleted folder {folderPath}")
            self.listWidget.addItem(item)
        for filePath in fileInFolders:
            item = QListWidgetItem(f"Deleted file {filePath}")
            self.listWidget.addItem(item)
        self.setListSourceFolders()
    
    def infoDeletedFiles(self, filePaths):
        if not filePaths:
            return
        for filePath in filePaths:
            item = QListWidgetItem(f"Deleted file {filePath}")
            self.listWidget.addItem(item)
    
    def setListSourceFolders(self):
        self.source.clear()
        listFolders = list(self.listDir.keys())
        for pathFolder in listFolders:
            if pathFolder == os.path.abspath(self.rootDir).replace("\\", "/"):
                continue
            self.source.addItem(pathFolder)
        
        self.onchangeFolderToCopy(0)
        self.source.currentIndexChanged.connect(self.onchangeFolderToCopy)
    
    def onchangeFolderToCopy(self, index):
        self.destination.clear()
        choosedFolder = self.source.itemText(index)
        if choosedFolder == "":
            return
        
        for pathFolder, level in self.listDir.items():
            if level >= self.listDir[choosedFolder] and pathFolder != choosedFolder and pathFolder != os.path.abspath(self.rootDir).replace("\\", "/"):
                self.destination.addItem(pathFolder)
    
    def copy_file_securely(self):
        src = self.source.currentText()
        dst = self.destination.currentText()
        if not dst:
            return
        src_level = self.listDir[src]
        dst_level = self.listDir[dst]

        if src_level > dst_level:
            QMessageBox.critical(self, "Error!", "No Write Down: Copying from high to lower\n security levels is not allowed.")
            return
        
        list_file_of_dst = [file for file in os.listdir(dst) if os.path.isfile(os.path.join(dst, file))]
        for pathFolder, level in self.listDir.items():
            if os.path.commonpath([src]) == os.path.commonpath([src, pathFolder]) and level <= src_level:
                for entry in os.listdir(pathFolder):
                    src_entry = os.path.join(pathFolder, entry).replace("\\", "/")
                    nameFile = entry.replace(".", f"_of_{os.path.basename(pathFolder)}.")
                    dst_entry = os.path.join(dst, nameFile).replace("\\", "/")
                    if os.path.isfile(src_entry):
                        try:
                            shutil.copy(src_entry, dst_entry)
                            item = QListWidgetItem(f"Copied file {src_entry} to folder {dst}.")
                            self.listWidget.addItem(item)
                            list_file_of_dst.append(entry)
                        except Exception as e:
                            QMessageBox.critical(self, "Error!", f"Error copying file\n {src_entry} to folder {dst}!")
        QMessageBox.information(self, "Success!", f"Successfully copied file\n from folder {src} to folder {dst}!")
               
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.createWindow and self.createWindow.isVisible():
                self.createWindow.close()
            if self.changeWindow and self.changeWindow.isVisible():
                self.changeWindow.close()
            if self.deleteWindow and self.deleteWindow.isVisible():
                self.deleteWindow.close()
                
            event.accept()
        else:
            event.ignore()

    def addLvl(self):
        dialog = DialogChange("Add level")
        dialog.name_label.setText("Enter name secret:")
        dialog.exec_()
        if not dialog.newName:
            return
        name = dialog.newName

        itemList = [self.level.itemText(i) for i in range(self.level.count())]
        if name and (name not in itemList):
            self.level.addItem(name)
        else:
            QMessageBox.critical(self, "Error", "Corrupted name!")
    
    def delLvl(self):
        level_ = self.level.currentIndex()
        if (level_ == 0):
            QMessageBox.critical(self, "Error", "Default secrecy level cannot be deleted!")
            return
        self.level.removeItem(self.level.currentIndex())
        for pathFolder, level in self.listDir.items():
            if level == level_:
                self.listDir[pathFolder] = 0
            if level > level_:
                self.listDir[pathFolder] -= 1
        
    def renameLvl(self):
        index = self.level.currentIndex()
        if (index == 0):
            QMessageBox.critical(self, "Error", "Default secrecy level cannot be renamed!")
            return
        dialog = DialogChange("Rename Level")
        dialog.name_label.setText("Enter new name:")
        dialog.exec_()
        if not dialog.newName:
            return
        name = dialog.newName
        itemList = [self.level.itemText(i) for i in range(self.level.count())]
        if name not in itemList:
            self.level.setItemText(index, name)
        else:
            QMessageBox.critical(self, "Error", "Name is taken!")
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow()
    ui.show()
    sys.exit(app.exec_())