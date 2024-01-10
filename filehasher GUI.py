import os, hashlib, time
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
import ctypes

####FILE HASHING PROGRAM
####Version .5


####Functions

def runHasher():
    start_time = time.time()
    call.display.setText('Running Hasher............Please Wait...........\n')
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
            call.display.setText(f'Error: Unable to walk directory {targetName}')
    elif validateTarget(targetName, runType) == False:
        call.display.setText('Error: Invalid Target')
    end_time = time.time()
    call.display.append(f"Total Time: {end_time - start_time} seconds.")
   
               

def fileWalk(targetName, exportMode, alg, runType):
    file_count = 0
    byte_count = 0
    if exportMode == '1':
        fileExt = '.txt'
    elif exportMode == '2':
        fileExt = '.csv'
    if exportMode == '3':
        if runType == 'directory':
            for (r,d,f) in os.walk(targetName):
                for x in f:
                    filePath = os.path.join(r, x)
                    hashValue = hasher(filePath, alg)
                    file_count += 1
                    file_size = os.stat(filePath)[6]
                    byte_count += file_size
                    call.display.append(f'{filePath}:  {hashValue}')  
        elif runType == 'file':
            hashValue = hasher(targetName, alg)
            file_count += 1
            file_size = os.stat(filePath)[6]
            byte_count += file_size
            call.display.append(f'{targetName}:  {hashValue}')
    else:    
        with open(f'{userProfile}//Desktop/HashList{fileExt}', 'w') as F:
            if runType == 'directory':
                for (r,d,f) in os.walk(targetName):
                    if exportMode == '1':
                        for x in f:
                            filePath = os.path.join(r, x)
                            hashValue = hasher(filePath, alg)
                            file_count += 1
                            file_size = os.stat(filePath)[6]
                            byte_count += file_size                            
                            call.display.append(f'{filePath}:  {hashValue}\n')
                            print(f'{hashValue}', file = F)
                    elif exportMode == '2':
                        for x in f:
                            filePath = os.path.join(r, x)
                            hashValue = hasher(filePath, alg)
                            file_count += 1
                            file_size = os.stat(filePath)[6]
                            byte_count += file_size                            
                            call.display.append(f'{filePath}:  {hashValue}')
                            print(f'{hashValue}', file = F)
            elif runType == 'file':
                if exportMode == '1':
                    hashValue = hasher(filePath, alg)
                    file_count += 1
                    file_size = os.stat(filePath)[6]
                    byte_count += file_size
                    call.display.append(f'{filePath}:  {hashValue}\n')
                    print(f'{hashValue}', file = F)
                elif exportMode == '2':
                    hashValue = hasher(filePath, alg)
                    file_count += 1
                    file_size = os.stat(filePath)[6]
                    byte_count += file_size                    
                    call.display.append(f'{filePath}:  {hashValue}')
                    print(f'{filePath}, {hashValue}', file = F)
            call.display.append('Hashing Complete.')
    call.display.append('\nHashing Complete')
    call.display.append(f'Files Hashed: {file_count}')
    call.display.append(f'Bytes Hashed: {byte_count}')


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
                call.display.append('Error: Invalid Hashing Algorithm')
    except:
        call.display.append(f'Error Hashing File: {file}')


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

