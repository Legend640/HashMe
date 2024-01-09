import os, hashlib
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
import ctypes

####FILE HASHING PROGRAM
#
#
#

####Functions

def hasher(file, alg):
    md5Hash = hashlib.md5()
    sha1Hash = hashlib.sha1()
    sha256Hash = hashlib.sha256()
    try:
        with open (file, 'rb') as f:
            data = f.read()
            if alg == 'md5':
                md5Hash.update(data)
                return md5Hash.hexdigest()
            elif alg == 'sha1':
                sha1Hash.update(data)
                return sha1Hash.hexdigest()
            elif alg == 'sha256':
                sha256Hash.update(data)
                return sha256Hash.hexdigest()
            else:
                print('Invalid Hashing Algorithm')
    except:
        print('Error Hashing File')


def validateTarget(target, runType):
    if runType == 'directory':
        if os.path.isdir(target) == True:
            return True
        else:
            return False
    elif runType == 'file':
        if os.path.isfile(target) == True:
            return True
        else:
            return False

def runHasher():
    if call.directory_button.isChecked() == True:
        runType = 'directory'
    elif call.file_button.isChecked() == True:
        runType = 'file'    
    if call.name.text() == '':
        call.display.setText('File//Directory Field Must Not Be Blank')
    elif call.name.text() != '':
        targetName = call.name.text()
    if call.md5_box.isChecked():
        alg = 'md5'
    elif call.sha1_box.isChecked():
        alg = 'sha1'
    if call.text_box.isChecked():
        exportMode = '1'
    elif call.csv_box.isChecked():
        exportMode = '2'
    elif call.displayonly_box.isChecked():
        exportMode = '3'
    if validateTarget(targetName, runType):
        try:
            fileWalk(targetName, exportMode, alg, runType)
        except:
            call.display.setText(f'Unable to walk directory: {targetName}')
    elif validateTarget(targetName, runType) == False:
        call.display.setText('Invalid Target')
               

def fileWalk(targetName, exportMode, alg, runType):
    if exportMode == '1':
        fileExt = '.txt'
    elif exportMode == '2':
        fileExt = '.csv'
    if exportMode == '3':
        call.display.setText('Running Hasher')
        if runType == 'directory':
            for (r,d,f) in os.walk(targetName):
                for x in f:
                    filePath = os.path.join(r, x)
                    hashValue = hasher(filePath, alg)
                    call.display.append(f'{filePath}:  {hashValue}')  
        elif runType == 'file':
            print(f"file hashing, {targetName}, {alg}")
            hashValue = hasher(targetName, alg)
            call.display.append(f'{targetName}:  {hashValue}')
    else:    
        with open(f'{userProfile}//Desktop/HashList{fileExt}', 'w') as F:
            call.display.setText('Running Hasher')
            if runType == 'directory':
                for (r,d,f) in os.walk(targetName):
                    if exportMode == '1':
                        for x in f:
                            filePath = os.path.join(r, x)
                            hashValue = hasher(filePath, alg)
                            call.display.append(f'{filePath}:  {hashValue}\n')
                            print(f'{hashValue}', file = F)
                    elif exportMode == '2':
                        for x in f:
                            filePath = os.path.join(r, x)
                            hashValue = hasher(filePath, alg)
                            call.display.append(f'{filePath}:  {hashValue}')
                            print(f'{filePath}, {hashValue}', file = F)
            elif runType == 'file':
                if exportMode == '1':
                    hashValue = hasher(filePath, alg)
                    call.display.append(f'{filePath}:  {hashValue}\n')
                    print(f'{hashValue}', file = F)
                elif exportMode == '2':
                    hashValue = hasher(filePath, alg)
                    call.display.append(f'{filePath}:  {hashValue}')
                    print(f'{filePath}, {hashValue}', file = F)

def fileBrowser():
    if call.directory_button.isChecked() == True:
        targetName = QtWidgets.QFileDialog.getExistingDirectory(None,"Open Directory", userProfile)
        call.name.setText(targetName)
    elif call.file_button.isChecked() == True:
        targetName = QtWidgets.QFileDialog.getOpenFileName(None,"Open File", userProfile)
        call.name.setText(targetName[0])


####Main 
ctypes.windll.shcore.SetProcessDpiAwareness(0)
app = QtWidgets.QApplication([])
call = uic.loadUi('gui.ui')
call.show()
userProfile = os.environ['USERPROFILE']
call.hash_button.clicked.connect(runHasher)
call.browse.clicked.connect(fileBrowser)
app.exec()

