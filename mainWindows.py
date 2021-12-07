from PyQt5.QtWidgets import QDialog, QFileDialog, QMenu, QWidget, QVBoxLayout, QStackedWidget, QLabel
from PyQt5.QtCore import Qt, QPoint, QRect, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QFont
from os.path import isfile, join, isdir
from Ui.py_toggle import PyToggle
from shutil import copy, rmtree
from PyQt5.uic import loadUi
from Server import *
import cv2
import os

import threading
mutex = threading.Lock()


class transistor:
    def __init__(self, widget, id = None):
        self.widget = widget
        self.id = id

    def showLogin(self, event= None):
        logWindow = login(self.widget)
        if self.id: self.quitEvent()
        self.widget.addWidget(logWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showSign(self, event = None):
        signWindow = sign(self.widget)
        self.widget.addWidget(signWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showChange(self, event = None):
        changePassWindow = changePass(self.widget)
        self.widget.addWidget(changePassWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showCamera(self, id, dataAllowed):
        initialAllowCameraWindow = initialAllowCamera(self.widget, id, dataAllowed)
        self.widget.addWidget(initialAllowCameraWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showData(self, id):
        initialAllowDataWindow = initialAllowData(self.widget, id)
        self.widget.addWidget(initialAllowDataWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showPresentations(self, event = None):
        presentationsWindow = presentations(self.widget, self.id)
        self.widget.addWidget(presentationsWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showFiles(self, event = None):
        filewindow = files(self.widget, self.id)
        self.widget.addWidget(filewindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showCollab(self, event = None):
        collabswindow = collabs(self.widget, self.id)
        self.widget.addWidget(collabswindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showRooms(self, event = None):
        roomswindow = rooms(self.widget, self.id)
        self.widget.addWidget(roomswindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showUser(self, event = None):
        userwindow = userData(self.widget, self.id)
        self.widget.addWidget(userwindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showSettings(self, event = None):
        settingswindow = meetSettings(self.widget, self.id)
        self.widget.addWidget(settingswindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def showPrecedent(self, event = None):
        newIndex = self.widget.currentIndex() - 1
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.setCurrentIndex(newIndex)

    def quitEvent(self, event = None):
        idRoom = isConnectedServer(self.id)
        if idRoom: leaveRoomServer(self.id, idRoom)



class getStarted(QDialog):
    def __init__(self, widget):
        self.widget = widget
        self.transistor = transistor(self.widget)
        # Load ui and widget network
        super(getStarted, self).__init__()
        loadUi('Ui/Get_Started.ui', self)

        # Labels/Buttons Events
        self.startBtn.clicked.connect(self.transistor.showLogin)




# Account access
class login(QDialog):
    def __init__(self, widget):
        super(login, self).__init__()

        # Load ui and widget network
        loadUi('Ui/LogIn.ui', self)
        self.transistor = transistor(widget)

        # Labels Events
        self.loginBtn.clicked.connect(self.showNext)
        self.signLabel.mousePressEvent = self.transistor.showSign
        self.forgotLabel.mousePressEvent = self.transistor.showChange

        # Define local preference
        self.preferences = []
        self.blob = BinaryBlob()

    def checkAccount(self):
        if self.emailInput.text() == '' and self.passInput.text() == '':
            self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
        elif self.emailInput.text() == '':
            self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.passInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        elif self.passInput.text() == '':
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.emailInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        else:
            try:

                result = loginServer(self.emailInput.text(), self.passInput.text())
                if result == []:
                    self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
                    self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
                    self.emailInput.setPlaceholderText("Invalid email")
                    self.passInput.setPlaceholderText("Invalid password")
                    self.emailInput.setText('')
                    self.passInput.setText('')
                    return False


                self.id = result[0]
                self.preferences = result[1]


                self.emailInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
                self.emailInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
                return True
            except Exception as e:
                print(e)
                print('Error! We\'re sorry you can\'t connect to the database')
                self.emailInput.setText('')
                self.passInput.setText('')
                self.emailInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
                self.passInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
                return False

        print('Login failed')
        self.emailInput.setPlaceholderText("Enter your user name or email")
        self.passInput.setPlaceholderText("Enter your password")
        return False

    def deleteFiles(self):
        folder = os.getcwd() + '\\PresentationFiles'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def uploadFromDB(self):
        self.deleteFiles()
        data = getFilesServer(self.id)
        for filename, file in data:
            self.blob.writeToFile(file, str(os.getcwd()) + r'\PresentationFiles\\' + filename)
            self.blob.transformIntoImg(str(os.getcwd()) + r'\PresentationFiles/' + filename)

    def showNext(self):
        if self.checkAccount():
            self.uploadFromDB()
            if not self.preferences[0]:
                self.transistor.showCamera(self.id, self.preferences[1])

            elif not self.preferences[1]:
                self.transistor.showData(self.id)
            else:
                self.transistor.id = self.id
                self.transistor.showPresentations()


class sign(QDialog):
    def __init__(self, widget):
        super(sign, self).__init__()


        # Load ui and widget network
        self.transistor = transistor(widget)
        self.blob = BinaryBlob()
        loadUi('Ui/SignUp.ui', self)

        # Labels Events
        self.signBtn.clicked.connect(self.showNext)
        self.logLabel.mousePressEvent = self.transistor.showLogin

    def deleteFiles(self):
        folder = os.getcwd() + '/PresentationFiles'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def showNext(self):
        if self.checkAccount():
            self.transistor.showCamera(self.id, False)

    def reset_ui(self):
        self.nameInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        self.emailInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        self.passInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        self.confInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        self.nameInput.setPlaceholderText("Enter your user name")
        self.emailInput.setPlaceholderText("Enter your useremail")
        self.passInput.setPlaceholderText("Enter your password")
        self.confInput.setPlaceholderText("Confirm the password")

    def checkAccount(self):
        self.reset_ui()
        if self.nameInput.text() == '':
            self.nameInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            return False
        if self.emailInput.text() == '':
            self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            return False
        if self.passInput.text() == '':
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            return False
        if self.confInput.text() == '':
            self.confInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            return False
        if self.passInput.text() != self.confInput.text():
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.confInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.passInput.setText('')
            self.confInput.setText('')
            self.confInput.setPlaceholderText('The password should be identic')
            return False

        if len(self.nameInput.text()) < 4:
            self.nameInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.nameInput.setPlaceholderText("Minimum 4 Charachters")
            return False
        if len(self.emailInput.text()) < 4:
            self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.emailInput.setPlaceholderText("Minimum 4 Charachters")
            return False
        if len(self.passInput.text()) < 4:
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.passInput.setPlaceholderText("Minimum 4 Charachters")
            return False
        if len(self.confInput.text()) < 4:
            self.confInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.confInput.setPlaceholderText("Minimum 4 Charachters")
            return False

        try:
            image = self.blob.convertToBinaryData(str(os.getcwd()) + r"\Ui\Images\profile_image.png")
            result = registerServer(self.nameInput.text(), self.emailInput.text(), self.passInput.text(), image)

            if result == []:
                self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
                self.emailInput.setText('')
                self.emailInput.setPlaceholderText("This email is already used")
                return False

            self.id = result
            return True

        except Exception as e:
            print('Error! We\'re sorry you can\'t connect to the database')
            print(e)
            self.nameInput.setText('')
            self.emailInput.setText('')
            self.passInput.setText('')
            self.confInput.setText('')

            self.nameInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
            self.emailInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
            self.passInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
            self.confInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
            return False


class changePass(QDialog):
    def __init__(self, widget):
        super(changePass, self).__init__()
        # Load ui and widget network
        loadUi('Ui/changePassword.ui', self)
        self.transistor = transistor(widget)
        self.blob = BinaryBlob()

        # Labels Events
        self.changeBtn.clicked.connect(self.showNext)
        self.cancelLabel.mousePressEvent = self.transistor.showLogin

    def reset_ui(self):
        self.emailInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        self.passInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        self.confInput.setStyleSheet("background-color: rgb(235, 220, 178, 200);")
        self.emailInput.setPlaceholderText("Enter your user email")
        self.passInput.setPlaceholderText("Enter new password")
        self.confInput.setPlaceholderText("Confirm new password")

    def checkAccount(self):
        self.reset_ui()

        if self.emailInput.text() == '':
            self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            return False
        if self.passInput.text() == '':
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            return False
        if self.confInput.text() == '':
            self.confInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            return False
        if self.passInput.text() != self.confInput.text():
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.confInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.passInput.setText('')
            self.confInput.setText('')
            self.confInput.setPlaceholderText('The password should be identic')
            return False

        if len(self.emailInput.text()) < 4:
            self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.emailInput.setPlaceholderText("Minimum 4 Charachters")
            return False
        if len(self.passInput.text()) < 4:
            self.passInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.passInput.setPlaceholderText("Minimum 4 Charachters")
            return False
        if len(self.confInput.text()) < 4:
            self.confInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
            self.confInput.setPlaceholderText("Minimum 4 Charachters")
            return False


        try:
            result = changePasswordServer(self.emailInput.text(), self.passInput.text())

            if result == []:
                self.emailInput.setStyleSheet("background-color: rgb(204, 22, 22);color:white;")
                self.emailInput.setPlaceholderText("This email is not used")
                return False

            self.id = result
            return True
        except:
            print('Error! We\'re sorry you can\'t connect to the database')
            self.emailInput.setText('')
            self.passInput.setText('')
            self.confInput.setText('')

            self.emailInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
            self.passInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
            self.confInput.setPlaceholderText("Error! We\'re sorry you can\'t connect to the database")
            return False

    def showNext(self):
        if self.checkAccount():
            self.uploadFromDB()
            self.transistor.id = self.id
            self.transistor.showPresentations()

    def deleteFiles(self):
        folder = os.getcwd() + '/PresentationFiles'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def uploadFromDB(self):
        self.deleteFiles()
        data = getFilesServer(self.id)
        for filename, file in data:
            self.blob.writeToFile(file, str(os.getcwd()) + r'\PresentationFiles\\' + filename)
            self.blob.transformIntoImg(str(os.getcwd()) + r'\PresentationFiles\'' + filename)




# Camera and Data permissions
class initialAllowCamera(QDialog):
    def __init__(self, widget, id, dataAllowed):
        super(initialAllowCamera, self).__init__()
        # Load ui and widget network
        loadUi('Ui/initialAllowCamera.ui', self)
        self.transistor = transistor(widget, id)

        # Labels Events
        self.allowBtn.mousePressEvent = self.allowCamera
        self.laterBtn.mousePressEvent = self.discardCamera

        # Define data allowed and user email
        self.dataAllowed = dataAllowed
        self.id = id

    def allowCamera(self, event):
        allowCameraServer(self.id)
        self.showNext()

    def discardCamera(self, event):
        self.showNext()

    def showNext(self):
        if self.dataAllowed:
            self.transistor.showPresentations()
        else:
            self.transistor.showData(self.id)


class initialAllowData(QDialog):
    def __init__(self, widget, id):
        super(initialAllowData, self).__init__()
        # Load ui and widget network
        loadUi('Ui/initialAllowData.ui', self)
        self.transistor = transistor(widget, id)

        # Labels Events
        self.allowBtn.mousePressEvent = self.allowData
        self.laterBtn.mousePressEvent = self.discardData

        # Define user email
        self.id = id

    def allowData(self, event):
        allowDataServer(self.id)
        self.transistor.showPresentations()

    def discardData(self, event):
        self.transistor.showPresentations()




# Main Windows
class presentations(QDialog):
    def __init__(self, widget, id):
        super(presentations, self).__init__()
        # Load ui and widget network
        loadUi('Ui/mainPresentation.ui', self)
        self.transistor = transistor(widget, id)
        self.widget = widget
        self.id = id
        self.checkState()
        self.widget.closeEvent = self.transistor.quitEvent


        # Labels Events
        self.filesLabel.mousePressEvent = self.transistor.showFiles
        self.collabLabel.mousePressEvent = self.transistor.showCollab
        self.roomsLabel.mousePressEvent = self.transistor.showRooms
        self.filesIcon.mousePressEvent = self.transistor.showFiles
        self.collabIcon.mousePressEvent = self.transistor.showCollab
        self.roomsIcon.mousePressEvent = self.transistor.showRooms
        self.userIcon.mousePressEvent = self.contextMenu
        self.joinBtn.clicked.connect(self.connect)
        self.leaveBtn.clicked.connect(self.leaveRoom)
        self.arrowIcon.mousePressEvent = self.transistor.showPrecedent


        # Define user id
        self.id = id

    def connect(self):
        preferences = getPreferencesServer(self.id)
        if preferences != []:
            checkPermissions(self.id, preferences, self.window(), self.widget)

    def checkState(self):
        print('here')
        name, self.idRoom = getRoomNameServer(self.id)
        print(name)
        if name == []:
            self.leaveBtn.setHidden(True)
            self.warningBox.setHidden(True)
        else:
            self.leaveBtn.setHidden(False)
            self.warningBox.setHidden(False)
            self.warningBox.setText('Currently you are in the room: '+name)

    def leaveRoom(self):
        leaveRoomServer(self.id, self.idRoom)
        self.widget.removeWidget(self.widget.currentWidget())
        self.transistor.showPresentations()

    def contextMenu(self, event):
        if event.button() == Qt.RightButton:
            print('Right')
            self.contextMenu = QMenu()

            settings = self.contextMenu.addAction("Settings")
            translate = self.contextMenu.addAction("Translate")
            coll = self.contextMenu.addAction("Collaboration Platform")
            logout = self.contextMenu.addAction("Logout")


            self.contextMenu.setFixedWidth(200)
            action = self.contextMenu.exec_(self.mapToGlobal(QPoint(500, 30)))
            if action == logout:
                self.transistor.showLogin()
            elif action == settings:
                self.transistor.showSettings()
        else:
            print('Left')
            self.transistor.showUser()


class files(QDialog):
    def __init__(self, widget, id):
        super(files, self).__init__()
        # Load ui and widget network
        loadUi('Ui/mainFiles.ui', self)
        self.transistor = transistor(widget, id)
        self.widget = widget
        self.widget.closeEvent = self.transistor.quitEvent

        # Labels/Buttons Events
        self.presentationLabel.mousePressEvent = self.transistor.showPresentations
        self.collabLabel.mousePressEvent = self.transistor.showCollab
        self.roomsLabel.mousePressEvent = self.transistor.showRooms
        self.presentationIcon.mousePressEvent = self.transistor.showPresentations
        self.collabIcon.mousePressEvent = self.transistor.showCollab
        self.roomsIcon.mousePressEvent = self.transistor.showRooms
        self.arrowIcon.mousePressEvent = self.transistor.showPrecedent
        self.addLabel.mousePressEvent = self.addPresentation
        self.createLabel.mousePressEvent = self.addPresentation
        self.userIcon.mousePressEvent = self.contextMenu

        # Define user email
        self.id = id
        self.blob = BinaryBlob()

        self.setFiles()
        self.drawFiles()

    def addPresentation(self, event):
        file_filter = 'Presentation File(*.ppt *pptx);; Pdf File (*pdf)'
        self.setFiles()
        if len(self.file) < 5:
            response = QFileDialog.getOpenFileNames(
                parent=self,
                caption='Select a file',
                directory= os.getcwd(),
                filter = file_filter
            )

            if len(response[0]) > 5 - len(self.file):
                response = response[0][:5 - len(self.file)]
            else:
                response = response[0]
            print(response)

            for path in response:
                copy(path, str(os.getcwd()) + r'\PresentationFiles')
                self.addFilesDB(os.path.basename(path))
                self.blob.transformIntoImg(str(os.getcwd()) + r'\PresentationFiles/' + os.path.basename(path))

            self.drawFiles()

            self.widget.removeWidget(self.widget.currentWidget())
            self.transistor.showFiles()

    def addFilesDB(self, fileName):
        try:
            bFile = self.blob.convertToBinaryData(str(os.getcwd()) + r'\PresentationFiles\\' + fileName)
            loadFilesServer(self.id, fileName, bFile)
        except:
            print("Oops...Something went wrong")

    def contextMenu(self, event):
        if event.button() == Qt.RightButton:
            print('Right')
            self.contextMenu = QMenu()

            settings = self.contextMenu.addAction("Settings")
            translate = self.contextMenu.addAction("Translate")
            coll = self.contextMenu.addAction("Collaboration Platform")
            logout = self.contextMenu.addAction("Logout")


            self.contextMenu.setFixedWidth(200)
            action = self.contextMenu.exec_(self.mapToGlobal(QPoint(500, 30)))
            if action == logout:
                self.transistor.showLogin()
            elif action == settings:
                self.transistor.showSettings()

        else:
            print('Left')
            self.transistor.showUser()

    def setFiles(self):
        path = os.getcwd() + '/PresentationFiles'
        self.file = [f for f in os.listdir(path) if isfile(join(path, f))]
        self.dirs = [f for f in os.listdir(path) if isdir(join(path, f))]

    def drawFiles(self):
        self.setFiles()
        icons = fileIcons(self.window(), self.file, self.menu)
        icons.addElements()

        self.addLabel.setGeometry((len(self.file) % 3 + 1) * 180, 70 + 120 * (len(self.file) // 3), 130, 80)
        self.createLabel.setGeometry((len(self.file) % 3 + 1) * 180, 50 + 120 * (len(self.file)//3), 135, 20)

    def menu(self, event):
        if event.button() == Qt.RightButton:
            print('Right')
            self.contextMenu = QMenu()
            delete = self.contextMenu.addAction("Delete")
            action = self.contextMenu.exec_(event.globalPos())
            if action == delete:
                self.delete(event.windowPos().x(), event.windowPos().y())

    def delete(self, positionX, positionY):
        itemX = int((positionX//180) -1)
        itemY = 0 if positionY < 160 else 1
        index = itemX+itemY*3
        print(str(os.getcwd()) + '\\PresentationFiles\\' + self.file[index])
        file = self.blob.convertToBinaryData(str(os.getcwd()) + '\\PresentationFiles\\' + self.file[index])
        deleteFileServer(self.id, self.file[index], file)
        os.remove(str(os.getcwd()) + '\\PresentationFiles\\' + self.file[index])

        filepath = self.file[index].split(sep='.')[0]
        print(filepath)
        folder = os.getcwd() + '/PresentationFiles/' + filepath
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    rmtree(file_path)
                if len(os.listdir(folder)) == 0:
                    os.rmdir(folder)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        self.widget.removeWidget(self.widget.currentWidget())
        self.transistor.showFiles()


class collabs(QDialog):
    def __init__(self, widget, id):
        super(collabs, self).__init__()
        # Load ui and widget network
        loadUi('Ui/mainCollab.ui', self)
        self.transistor = transistor(widget, id)
        self.widget = widget
        self.widget.closeEvent = self.transistor.quitEvent


        # Labels/Buttons Events
        self.presentationLabel.mousePressEvent = self.transistor.showPresentations
        self.filesLabel.mousePressEvent = self.transistor.showFiles
        self.roomsLabel.mousePressEvent = self.transistor.showRooms
        self.presentationIcon.mousePressEvent = self.transistor.showPresentations
        self.filesLabel.mousePressEvent = self.transistor.showFiles
        self.roomsIcon.mousePressEvent = self.transistor.showRooms
        self.arrowIcon.mousePressEvent = self.transistor.showPrecedent
        self.userIcon.mousePressEvent = self.contextMenu

        # Define user email
        self.id = id
        self.drawIcons()

    def drawIcons(self):
        self.data = getCollabsServer(self.id)

        try:
            self.icons = collabIcons(self.window(), self.data)
            self.icons.addElements()
            print('Loaded')
        except Exception as e:
            print('Failed')
            print(e)

    def contextMenu(self, event):
        if event.button() == Qt.RightButton:
            print('Right')
            self.contextMenu = QMenu()

            settings = self.contextMenu.addAction("Settings")
            translate = self.contextMenu.addAction("Translate")
            coll = self.contextMenu.addAction("Collaboration Platform")
            logout = self.contextMenu.addAction("Logout")


            self.contextMenu.setFixedWidth(200)
            action = self.contextMenu.exec_(self.mapToGlobal(QPoint(500, 30)))
            if action == logout:
                self.transistor.showLogin()
            elif action == settings:
                self.transistor.showSettings()


        else:
            print('Left')
            self.transistor.showUser()


class rooms(QDialog):
    def __init__(self, widget, id):
        super(rooms, self).__init__()
        # Load ui and widget network
        loadUi('Ui/mainRooms.ui', self)
        self.widget = widget
        self.id = id
        self.transistor = transistor(widget, id)
        self.widget.closeEvent = self.transistor.quitEvent

        # Labels/Buttons Event
        self.setEvents()
        self.drawRooms()

    def setEvents(self):
        self.presentationLabel.mousePressEvent = self.transistor.showPresentations
        self.filesLabel.mousePressEvent = self.transistor.showFiles
        self.collabLabel.mousePressEvent = self.transistor.showCollab
        self.presentationIcon.mousePressEvent = self.transistor.showPresentations
        self.filesLabel.mousePressEvent = self.transistor.showFiles
        self.collabIcon.mousePressEvent = self.transistor.showCollab
        self.arrowIcon.mousePressEvent = self.transistor.showPrecedent
        self.userIcon.mousePressEvent = self.contextMenu

        self.createBtn.clicked.connect(self.createRoom)
        self.joinBtn.clicked.connect(self.joinRoom)

    def setRooms(self):
        self.admin = getRoomsAdminServer(self.id)
        self.participant = getRoomsParticipantsServer(self.id)
        self.data = self.admin + self.participant

    def drawRooms(self):
        self.setRooms()
        self.roomIcons = roomIcons(self.window(), self.data, menu=self.menu)
        self.roomIcons.addElements()
        self.addRoom.setGeometry(190, 100 + 40*len(self.data), 450, 45)
        self.keyInput.setGeometry(440, 110 + 40 * len(self.data), 200, 25)
        self.createBtn.setGeometry(480, 160 + 40 * len(self.data), 65, 30)
        self.joinBtn.setGeometry(575, 160 + 40 * len(self.data), 65, 30)

    def contextMenu(self, event):
        if event.button() == Qt.RightButton:
            print('Right')
            self.contextMenu = QMenu()

            settings = self.contextMenu.addAction("Settings")
            translate = self.contextMenu.addAction("Translate")
            coll = self.contextMenu.addAction("Collaboration Platform")
            logout = self.contextMenu.addAction("Logout")


            self.contextMenu.setFixedWidth(200)
            action = self.contextMenu.exec_(self.mapToGlobal(QPoint(500, 30)))
            if action == logout:
                self.transistor.showLogin()
            elif action == settings:
                self.transistor.showSettings()


        else:
            print('Left')
            self.transistor.showUser()

    def menu(self, event):
        if event.button() == Qt.RightButton:
            print('Right')
            self.contextMenu = QMenu()
            leave = self.contextMenu.addAction("Leave")
            action = self.contextMenu.exec_(event.globalPos())
            if action == leave:
                index = int((event.windowPos().y()-100)//40)
                deleteRoomServer(self.id,self.data[index][0], index<len(self.admin))
                print('yep')
                self.widget.removeWidget(self.widget.currentWidget())
                self.transistor.showRooms()

    def createRoom(self):
        createRoomServer(self.id, self.keyInput.text())
        self.widget.removeWidget(self.widget.currentWidget())
        self.transistor.showRooms()

    def joinRoom(self):
        joinRoomServer(self.id, self.keyInput.text())
        self.widget.removeWidget(self.widget.currentWidget())
        self.transistor.showRooms()





# Personal windows
class userData(QDialog):
    def __init__(self, widget, id):
        super(userData, self).__init__()
        # Load ui and widget network
        loadUi('Ui/userData.ui', self)
        self.widget = widget
        self.transistor = transistor(widget, id)
        self.widget.closeEvent = self.transistor.quitEvent

        # Labels/Buttons Events
        self.meetLabel.mousePressEvent = self.transistor.showSettings
        self.arrowIcon.mousePressEvent = self.transistor.showPrecedent

        # Define user email
        self.id = id
        self.blob = BinaryBlob()
        self.setData()

    def setData(self):
        data = getUserDataServer(self.id)

        self.blob.imageTofile(data[2], 'user')
        self.blob.convertToPhoto(str(os.getcwd())+r'\Ui\Images\user.bin', True)

        self.nameLabel.setText(data[0])
        self.emailLabel.setText(data[1])
        self.imageLabel.setPixmap(QPixmap(r'Ui\Images\user.png'))


class meetSettings(QDialog):
    def __init__(self, widget, id):
        super(meetSettings, self).__init__()
        # Load ui and widget network
        loadUi('Ui/meetSettings.ui', self)
        self.widget = widget
        self.transistor = transistor(widget, id)
        self.widget.closeEvent = self.transistor.quitEvent

        self.drawButtons(self.window())

        # # Labels/Buttons Events
        self.profileLabel.mousePressEvent = self.transistor.showUser
        # self.arrowIcon.mousePressEvent = self.showPresentations
        self.arrowIcon.mousePressEvent = self.transistor.showPrecedent

        self.translateBtn.stateChanged.connect(self.changeState)
        self.attendanceBtn.stateChanged.connect(self.changeState)
        self.moodBtn.stateChanged.connect(self.changeState)
        self.presentationBtn.stateChanged.connect(self.changeState)
        self.graphBtn.stateChanged.connect(self.changeState)
        self.sportBtn.stateChanged.connect(self.changeState)

        # Define user email
        self.id = id
        self.loadSettings()

    def loadSettings(self):
        options = getSettingsServer(self.id)

        if options[0] : self.translateBtn.setChecked(True)
        if options[1]: self.attendanceBtn.setChecked(True)
        if options[2]: self.moodBtn.setChecked(True)
        if options[3]: self.presentationBtn.setChecked(True)
        if options[4]: self.graphBtn.setChecked(True)
        if options[5]: self.sportBtn.setChecked(True)

    def changeState(self):
        translate = 1 if self.translateBtn.isChecked() else 0
        attendance = 1 if self.attendanceBtn.isChecked() else 0
        mood = 1 if self.moodBtn.isChecked() else 0
        presentation = 1 if self.presentationBtn.isChecked() else 0
        graph = 1 if self.graphBtn.isChecked() else 0
        sport = 1 if self.sportBtn.isChecked() else 0

        settings = (translate, attendance, mood, presentation, graph, sport)
        updateSettingsServer(self.id, settings)

    def drawButtons(self, Dialog):

        self.container1 = QWidget(Dialog)
        self.layout1 = QVBoxLayout()
        self.translateBtn = PyToggle()
        self.translateBtn.setObjectName("translateBtn")
        self.layout1.addWidget(self.translateBtn)
        self.container1.setGeometry(QRect(550, 88, 70, 50))
        self.container1.setLayout(self.layout1)

        self.container2 = QWidget(Dialog)
        self.layout2 = QVBoxLayout()
        self.attendanceBtn = PyToggle()
        self.attendanceBtn.setObjectName("attendanceBtn")
        self.layout2.addWidget(self.attendanceBtn)
        self.container2.setGeometry(QRect(550, 130, 70, 50))
        self.container2.setLayout(self.layout2)

        self.container3 = QWidget(Dialog)
        self.layout3 = QVBoxLayout()
        self.moodBtn = PyToggle()
        self.moodBtn.setObjectName("modBtn")
        self.layout3.addWidget(self.moodBtn)
        self.container3.setGeometry(QRect(550, 172, 70, 50))
        self.container3.setLayout(self.layout3)

        self.container4 = QWidget(Dialog)
        self.layout4 = QVBoxLayout()
        self.presentationBtn = PyToggle()
        self.presentationBtn.setObjectName("presentationBtn")
        self.layout4.addWidget(self.presentationBtn)
        self.container4.setGeometry(QRect(550, 216, 70, 50))
        self.container4.setLayout(self.layout4)

        self.container5 = QWidget(Dialog)
        self.layout5 = QVBoxLayout()
        self.graphBtn = PyToggle()
        self.graphBtn.setObjectName("graphBtn")
        self.layout5.addWidget(self.graphBtn)
        self.container5.setGeometry(QRect(550, 259, 70, 50))
        self.container5.setLayout(self.layout5)

        self.container6 = QWidget(Dialog)
        self.layout6 = QVBoxLayout()
        self.sportBtn = PyToggle()
        self.sportBtn.setObjectName("sportBtn")
        self.layout6.addWidget(self.sportBtn)
        self.container6.setGeometry(QRect(550, 302, 70, 50))
        self.container6.setLayout(self.layout6)

        QMetaObject.connectSlotsByName(Dialog)




# Mini windows
def checkPermissions(id, preferences, mainWindow, mainWidget):
    global widget
    widget = QStackedWidget()

    if not preferences[0]:
        camera = allowCamera(widget, id, preferences, mainWindow, mainWidget)
        widget.addWidget(camera)
    elif not preferences[1]:
        data = allowData(widget, id, preferences, mainWindow, mainWidget)
        widget.addWidget(data)
    else:
        room = chooseRoom(widget,id, mainWindow, mainWidget)
        widget.addWidget(room)

    widget.show()


class allowCamera(QDialog):
    def __init__(self, widget, id, preferences, window, mainWidget):
        super(allowCamera, self).__init__()
        # Load ui and widget network
        loadUi('Ui/AllowCamera.ui', self)
        self.widget = widget
        self.widget.setFixedHeight(175)
        self.widget.setFixedWidth(480)
        widget.setWindowTitle('CVM')
        widget.setWindowIcon(QIcon('Ui/Images/icon.png'))

        self.id = id
        self.preferences = preferences
        self.mainWidget = mainWidget
        self.Window = window
        self.Window.setEnabled(False)
        self.widget.closeEvent = self.enableQuit

        self.allowBtn.mousePressEvent = self.allowCamera
        self.laterBtn.mousePressEvent = self.discardamera

    def enableQuit(self, event=None):
        self.Window.setEnabled(True)

    def allowCamera(self, event):
        allowCameraServer(self.id)
        print(self.preferences)
        self.preferences = (1,0)
        self.showNext()

    def discardamera(self, event):
        print('Discarded')
        self.Window.setEnabled(True)
        self.widget.close()

    def showNext(self):
        if not self.preferences[1]:
            data = allowData(self.widget, self.id, self.preferences, self.Window, self.mainWidget)
            self.widget.addWidget(data)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        else:
            room = chooseRoom(self.widget, self.id, self.Window, self.mainWidget)
            widget.addWidget(room)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


class allowData(QDialog):
    def __init__(self, widget, id, preferences, window, mainWidget):
        super(allowData, self).__init__()
        # Load ui and widget network
        loadUi('Ui/allowDataUse.ui', self)
        self.widget = widget
        self.widget.setFixedHeight(175)
        self.widget.setFixedWidth(480)
        widget.setWindowTitle('CVM')
        widget.setWindowIcon(QIcon('Ui/Images/icon.png'))
        self.id = id
        self.Window = window
        self.Window.setEnabled(False)
        self.preferences = preferences
        self.mainWidget = mainWidget
        self.widget.closeEvent = self.enableQuit

        self.allowBtn.mousePressEvent = self.allowData
        self.laterBtn.mousePressEvent = self.discardData

    def enableQuit(self, event=None):
        self.Window.setEnabled(True)

    def allowData(self, event):
        allowDataServer(self.id)
        self.showNext()

    def discardData(self, event):
        print('Discarded')
        self.Window.setEnabled(True)
        self.widget.close()

    def showNext(self):
        room = chooseRoom(self.widget, self.id, self.Window, self.mainWidget)
        widget.addWidget(room)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


class chooseRoom(QDialog):
    def __init__(self, widget, id, window, mainWidget):
        super(chooseRoom, self).__init__()
        # Load ui and widget network
        loadUi('Ui/Choose_room.ui', self)
        self.widget = widget
        self.widget.setFixedHeight(320)
        self.widget.setFixedWidth(480)
        widget.setWindowTitle('CVM')
        widget.setWindowIcon(QIcon('Ui/Images/icon.png'))
        self.id = id
        self.mainWidget = mainWidget
        self.Window = window
        self.Window.setEnabled(False)
        self.transistor = transistor(self.mainWidget, self.id)
        self.drawRooms()
        self.chooseBtn.mousePressEvent = self.choose
        self.widget.closeEvent = self.enableQuit

    def enableQuit(self, event=None):
        self.Window.setEnabled(True)

    def setRooms(self):
        self.admin = getRoomsAdminServer(self.id)
        self.participant = getRoomsParticipantsServer(self.id)
        self.data = self.admin + self.participant

    def drawRooms(self):
        self.rooms = []
        self.setRooms()
        print(self.data)
        print(len(self.data))
        if len(self.data)>0:
            self.roomIcons = roomIcons(self.window(), self.data, mini=True)
            self.rooms = self.roomIcons.addElements()
        else:
            self.noLabel = QLabel(self.window())
            self.noLabel.setObjectName('noLabel')
            self.noLabel.setGeometry(30, 40, 400, 45)
            self.noLabel.setStyleSheet\
                ('#noLabel {\nborder: 2px solid  #662E1C;\nborder-style: solid none solid none;\npadding: 10px;\ncolor: #662E1C;\nbackground-color: rgb(243,234,209);\n}')
            self.noLabel.setCursor(QCursor(Qt.PointingHandCursor))
            self.noLabel.setText('You have no rooms')
            font = QFont()
            font.setFamily("Montserrat,sans-serif")
            font.setPointSize(11)
            self.noLabel.setFont(font)
            self.chooseBtn.setEnabled(False)

    def choose(self, event):
        for i in range(len(self.rooms)):
            if self.rooms[i].styleSheet() == 'border: 2px solid  #662E1C;\nborder-style: solid none solid none;\npadding: 10px;\ncolor: #af4425;\nbackground-color: #c49d5d;':
                res = activateServer(self.id, self.data[i][0], i<len(self.admin))
                self.widget.close()
                self.Window.setEnabled(True)
                self.mainWidget.removeWidget(self.widget.currentWidget())
                self.transistor.showPresentations()
                thread_CV2 = threading.Thread(target=CV2, args=(self.id,))
                thread_CV2.start()




class fileIcons():
    def __init__(self, Window, files, menu):
        self.titles = [QLabel(Window) for x in range(len(files) + 1)]
        self.icons = [QLabel(Window) for x in range(len(files) + 1)]
        self.window = Window
        self.files = files
        self.menu = menu

    def title_customize(self, index):
        if index < len(self.files):
            self.titles[index].setObjectName("title" + str(index))
            self.titles[index].setStyleSheet(
                '#title' + str(index) + '{color : #662E1C;}#title' + str(index) + ':hover {color : #af4425;}')
            self.titles[index].setGeometry((index % 3 + 1) * 180, 50 + 120 * (index // 3), 135, 20)
            self.titles[index].setCursor(QCursor(Qt.PointingHandCursor))
            self.titles[index].setText(self.files[index])

            self.titles[index].mousePressEvent = self.menu
        else:
            return

    def icon_customize(self, index):
        if index < len(self.files):
            self.icons[index].setObjectName("presentation" + str(index))
            self.icons[index].setGeometry((index % 3 + 1) * 180, 70 + 120 * (index // 3), 130, 80)
            self.icons[index].setPixmap(QPixmap(f"PresentationFiles/{self.files[index].split(sep='.')[0]}/Slide1.png"))
            self.icons[index].setCursor(QCursor(Qt.PointingHandCursor))
            self.icons[index].setText("")
            self.icons[index].setScaledContents(True)
            self.icons[index].setStyleSheet('#presentation' + str(
                index) + '{\nbackground-color:red; border: 0.5px solid #662E1C;\n	box-sizing: border-box;\n	border-radius: 5px;\n	padding: 0.5px;\n}\n#presentation' + str(
                index) + ':hover{\n	border: 5px solid #662E1C;\n}\n')
            self.index = index
            self.icons[index].mousePressEvent = self.menu
        else:
            return

    def addElements(self):
        for i in range(len(self.files)+1):
            self.title_customize(i)
            self.icon_customize(i)


class collabIcons():
    def __init__(self, Window, data):
        self.collabs = [QLabel(Window) for x in range(len(data))]
        self.photos = [QLabel(Window) for x in range(len(data))]
        self.views = [QLabel(Window) for x in range(len(data))]

        self.data = data
        self.photo = list()
        self.blob = BinaryBlob()

    def collab_customize(self, index):
        if index < len(self.data):
            self.collabs[index].setObjectName("collab" + str(index))
            self.collabs[index].setStyleSheet(
                '#collab' + str(
                    index) + '{\nborder: 2px solid  #662E1C;\nborder-style: solid none solid none;\npadding: 45px;\ncolor : #662E1C;\n}')
            self.collabs[index].setGeometry(190, 140 + 43 * index, 450, 45)
            self.collabs[index].setText(self.data[index][0])
            font = QFont()
            font.setFamily("Montserrat,sans-serif")
            font.setPointSize(11)
            self.collabs[index].setFont(font)
        else:
            return

    def photo_customize(self, index):
        if index < len(self.data):
            self.photos[index].setObjectName("foto" + str(index))
            self.photos[index].setGeometry(195, 145 + 43 * index, 35, 35)
            self.photos[index].setText("")

            self.blob.imageTofile(self.data[index][1], 'temp')
            self.blob.convertToPhoto(str(os.getcwd()) + r'\Ui\Images\temp.bin', True)

            self.photos[index].setStyleSheet('#foto' + str(index) + '{\nborder-radius:10px;\n}')
            self.photos[index].setPixmap(QPixmap(r'Ui\Images\temp.png'))
            self.photos[index].setScaledContents(True)
        else:
            return

    def views_customize(self, index):
        if index < len(self.data):
            self.views[index].setObjectName("view" + str(index))
            self.views[index].setGeometry(540, 145 + 43 * (index), 100, 35)
            self.views[index].setText("View projects")
            self.views[index].setStyleSheet('#view' + str(index) + '{\ncolor : #662E1C;\n}\n#view' + str(
                index) + ':hover {\nbackground-color: #af4425;\n}')
        else:
            return

    def addElements(self):
        for i in range(len(self.data)+1):
            self.collab_customize(i)
            self.photo_customize(i)
            self.views_customize(i)


class roomIcons():
    def __init__(self, Window, data, menu = None, mini=False):
        self.rooms = [QLabel(Window) for x in range(len(data))]
        self.admins = [QLabel(Window) for x in range(len(data))]
        self.data = data
        self.menu = menu
        self.mini = mini

    def room_customize(self, index):
        if index < len(self.data):
            self.rooms[index].setObjectName("room" + str(index))
            if self.mini:
                self.rooms[index].setGeometry(30, 50 + 40 * index, 400, 45)
                self.rooms[index].setStyleSheet('#room' + str(index) +
                 ' {\nborder: 2px solid  #662E1C;\nborder-style: solid none solid none;\npadding: 10px;\ncolor: #662E1C;\nbackground-color: rgb(243,234,209);\n}')
                self.rooms[index].setCursor(QCursor(Qt.PointingHandCursor))
                self.rooms[index].mousePressEvent = self.choosen
            else:
                self.rooms[index].setStyleSheet('#room' + str(
                    index) + ' {border: 2px solid  #662E1C;border-style: solid none solid none;padding: 10px;color : #662E1C;}')
                self.rooms[index].setGeometry(190, 100 + 40 * index, 450, 45)
                self.rooms[index].mousePressEvent = self.menu
                self.rooms[index].mouseDoubleClickEvent = self.changeLabel

            self.rooms[index].setText(self.data[index][0])
            font = QFont()
            font.setFamily("Montserrat,sans-serif")
            font.setPointSize(11)
            self.rooms[index].setFont(font)
        else:
            return

    def admin_customize(self, index):
        if index < len(self.data):
            self.admins[index].setObjectName("admin" + str(index))
            self.admins[index].setGeometry(470, 110 + 40 * (index), 150, 25)
            self.admins[index].setText('Admin : ' + str(self.data[index][1]))
            self.admins[index].setStyleSheet('color : #662E1C;\nfont-weight:bold;')
            self.admins[index].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        else:
            return

    def addElements(self):
        for i in range(len(self.data)):
            self.room_customize(i)
            if not self.mini: self.admin_customize(i)

        if self.mini : return self.rooms

    def changeLabel(self, event):
        index = int((event.windowPos().y() - 100) // 40)
        key = self.data[index][2]
        admin = self.data[index][1]

        if self.admins[index].text() == 'Admin : ' + admin:
            self.admins[index].setText('Key : ' + key)
        else:
            self.admins[index].setText('Admin : ' + admin)

    def choosen(self, event):
        index = int((event.windowPos().y() - 50) // 40)
        for i in range(len(self.rooms)):
            if i == index:
                self.rooms[i].setStyleSheet('border: 2px solid  #662E1C;\nborder-style: solid none solid none;\npadding: 10px;\ncolor: #af4425;\nbackground-color: #c49d5d;')
            else: self.rooms[i].setStyleSheet('border: 2px solid  #662E1C;\nborder-style: solid none solid none;\npadding: 10px;\ncolor: #662E1C;\nbackground-color: rgb(243,234,209);')



from pdf2image import convert_from_path 


class BinaryBlob:
    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def imageTofile(self, data, name):
        print(str(os.getcwd()) + '\\Ui\\Images\\' + 'user' + '.bin')
        with open(str(os.getcwd()) + '\\Ui\\Images\\' + name + '.bin', 'wb') as file:
            file.write(data)
        return file

    def convertToPhoto(self, file, save):
        image = cv2.imread(file)
        if save:
            cv2.imwrite(''.join(str(file).split(sep='.')[:-1]) + '.png', image)

        return image

    def writeToFile(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data) 

    

    def transformIntoImg(self, filename):
        extension = filename.split(sep='.')[-1]
        if 'ppt' in extension:
            try:
                from comtypes import client
            except:
                print("Install comtypes from http://sourceforge.net/projects/comtypes/%22")
                return 0

            canvas = filename
            f = os.path.abspath(canvas)
            if not os.path.exists(f):
                print("No such file!")
                return 0

            powerpoint = client.CreateObject('Powerpoint.Application')
            powerpoint.Presentations.Open(f)
            powerpoint.ActivePresentation.Export(f, 'PNG')
            powerpoint.ActivePresentation.Close()
            powerpoint.Quit()
        # elif 'pdf' in extension:
        #     # Store Pdf with convert_from_path function
        #     images = convert_from_path(filename) 
        #     os.mkdir('PresentationFiles/' + filename.split(sep='.')[:-1])
            
        #     for i in range(len(images)):
            
        #         # Save pages as images in the pdf
        #         images[i].save('Slide'+ str(i) +'.jpg', 'JPEG')

        #     print('pdf')

import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os 
import pyvirtualcam
from pyvirtualcam import PixelFormat
import skimage
from skimage import color, data
from VirtualMouse import Mouse
from main_menu import MainMenu

from finaltest import Prezentare
from paint import blackboard



def CV2(id):
    connected = isConnectedServer(id)       
    cap = cv2.VideoCapture(0) 
    w = 1280
    h = 720 
    cap.set(3, 1280)
    cap.set(4, 720)

    mouse = Mouse()
    _, img = cap.read() 
    mm = MainMenu(mouse,img)
    with pyvirtualcam.Camera(w, h, 30, fmt=PixelFormat.BGR, print_fps=False) as cam:
        print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')
        while connected:
            success, img = cap.read()    
            img = cv2.flip(img,1) 
            mouse.active(img)
            img = mm.activate(img,cap)
            if mm.closeBool:
            
                 leaveRoomServer(id,connected)
                   

            cam.send(img)
            cam.sleep_until_next_frame() 
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break 

            connected = isConnectedServer(2)
            print(connected)


