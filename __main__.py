from _imports import *

class App(QMainWindow):
    from lib.ocr import threadedOCR, processOCR, unthreadedOCR, runOCR
    from lib.ocr import outFinishOCR, outShowProgressOCR, outOCRSave, outOCRWrite, inOCRSet, inOCRWrite
    from lib.listening import toggleListening, listen
    from lib.listening import adjustForAmbientNoise, threadedListening, idle

    def __init__(self):
        super(App,self).__init__()
        self.title = 'Image Sorter'
        self.width = 640
        self.height = 480
        self.willCloseWindows = False

        self.gui = Gui(self)
        self.dialog = Dialog(self)
        self.dialog.setDialogInfoAbout(ABOUT)
        self.gui.createWindowMenuAndFooter()

        self.setupPaths()
        self.loadImages()
        self.dialog.setDialogInfoUsage(os.path.dirname(self.folderPath))

        self.curImageId = 0
        self.willCloseThread= False
        self.isListening = True
        self.deactivateListeningPermanently = False
        self.recognizedKeyword = None
        self.imageArrOCR = []
        self.imageArrOCRData = {}

        self.threadpool = QThreadPool()
        self.idealThreadCount = self.threadpool.maxThreadCount()
        self.threadpool.setMaxThreadCount(1)
        self.eventStop = threading.Event()

        self.adjustForAmbientNoise()
        self.gui.initUI()
        self.gui.updateImageUI()

        self.threadedListening()

        if START_DIALOG:
            self.dialog.dialogInfoUsage()    

    def resizeEvent(self, event):
        self.width = event.size().width()
        self.height = event.size().height()
        self.gui.updateImageUI(event.size().width()*0.7)

    def setupPaths(self):
        try: 
            self.imgPath = IMG_PATH
        except:
            dialogText1 = MSG["DIR_IMAGES"]
            self.dialog.dialogInfo(dialogText1)
            self.imgPath = str(QFileDialog.getExistingDirectory(self, dialogText1))            
        try:
            self.folderPath = FOLDER_PATH
        except:
            dialogText2 = MSG["DIR_FOLDERS"]
            self.dialog.dialogInfo(dialogText2)
            self.folderPath = str(QFileDialog.getExistingDirectory(self, dialogText2))


    def loadImages(self):
        try:
            self.imageArr = os.listdir(self.imgPath)
            if DS_STORE in self.imageArr:
                self.imageArr.remove(DS_STORE)
        except Exception as e:
            self.dialog.dialogFinalImage(str(e))

        self.imageCount = len(self.imageArr)
        self.sortedImgHistory = [None] * self.imageCount

    def getImageName(self):
        self.currImgName = self.imageArr[self.curImageId]
        self.currImg = self.imgPath+'/'+self.currImgName
        self.currImgDate = getTime(self.currImg)
        self.newImgName = ""
        self.ocrResult = ""

    def getChosenFolderElement(self, folderChosen):
        folderChosenIndex = self.folderNameList.index(folderChosen)
        sender = self.folderNames.itemAt(folderChosenIndex).widget()
        return sender

    def closeEvent(self, e=True):
        self.eventStop.set()
        if(not self.willCloseWindows):
            self.willCloseWindows = True
            text = MSG["DONT_CLOSE"]
            bgText = MSG["CLOSING"]
            messagebox = TimerMessageBox(self, CLOSING_TIMEOUT, text, bgText)
            messagebox.exec_()
    
    def closeThread(self):
        out("THREAD COMPLETE!")
        if not self.willCloseThread and self.recognizedKeyword is None:
            self.eventStop.clear()
        elif self.willCloseThread and self.recognizedKeyword is None:
            self.eventStop.clear()
            out("Closing")
        else:
            if self.curImageId < self.imageCount:
                self.nextImage(self.recognizedKeyword)

    def listeningProgress(self, s):
        out("progressCallback")
        if(s == 0):
            self.statusbar.showMessage(MSG["LISTENING"])
        elif (s == 1):
            if self.recognizedKeyword is not None:
                out(self.recognizedKeyword)
        elif (s == 2):
            self.imageActionText.setText(MSG["NOT_UNDERSTAND"])
            self.imageActionTextFade()
        elif (s == 3):
            self.imageActionText.setText(MSG["API_ERROR"])
            self.imageActionTextFade()
            #self.statusbar.showMessage("Could not understand")

    ''' ACTION HANDLER '''
    
    def keyPressEvent(self, e):
        #Pause
        if e.key() == Qt.Key_Space:
            #open line edit
            self.box.itemAt(1).widget().setVisible(False)
            self.lineEdit.setVisible(True)
            self.lineEdit.setFocus(True)
        #Previous
        if e.key() == Qt.Key_Left:
            if self.curImageId > 0:
                self.curImageId -= 1
                if self.sortedImgHistory[self.curImageId] is not None:
                    self.recognizedKeyword = self.sortedImgHistory[self.curImageId]["folderChosen"] 
                else: 
                    self.recognizedKeyword = None
                self.gui.updateImageUI()
                self.statusbar.showMessage('Previous Image')
        #Next
        if e.key() == Qt.Key_Right:
            if self.curImageId < len(self.sortedImgHistory)-1:
                self.curImageId += 1
                if self.sortedImgHistory[self.curImageId] is not None:
                    self.recognizedKeyword = self.sortedImgHistory[self.curImageId]["folderChosen"]
                else: 
                    self.recognizedKeyword = None
                self.gui.updateImageUI()
                self.statusbar.showMessage('Next Image')

    def returnPressed(self):
        self.newImgName = self.lineEdit.text()
        imageProgress = "("+str(self.curImageId+1)+"/"+str(self.imageCount)+")"
        imageNameText = imageProgress + " " + self.newImgName
        #close line edit
        self.box.itemAt(1).widget().setText(imageNameText)
        self.lineEdit.setFocus(False)
        self.lineEdit.setVisible(False)
        self.box.itemAt(1).widget().setVisible(True)

    ''' MAIN FUNCTIONS '''

    def nextImageManual(self):
        sender = self.sender()
        self.recognizedKeyword = sender.text()
        self.nextImage(self.recognizedKeyword)

    def nextImage(self, folderChosen):
        if self.isListening:
            if(self.curImageId > len(self.sortedImgHistory)-1):
                self.sortedImgHistory.append(None)

            imageInHistory = False
            if(self.imageCount > self.curImageId and self.sortedImgHistory[self.curImageId] != None):
                imageInHistory = True

            newImgName = self.currImgName
            if self.newImgName != "":
                filename, file_extension = os.path.splitext(self.currImgName)
                newImgName = self.newImgName+file_extension

            toDest = self.folderPath+"/"+folderChosen+"/"+newImgName

            if(imageInHistory):
                fromSrc = self.folderPath + "/" + self.sortedImgHistory[self.curImageId]["folderChosen"] + "/"+ self.sortedImgHistory[self.curImageId]["newImgName"]
            else:
                fromSrc = self.currImg

            if DEBUG is False:
                try:
                    if(imageInHistory):
                        dest = shutil.move(fromSrc, toDest)
                    else:
                        dest = shutil.copy(fromSrc, toDest)
                    out("Finished")
                except Exception as e:
                    out(e)
                    self.dialog.dialogInfo(MSG["ERROR_COPYING_PT1"], MSG["ERROR_COPYING_PT2"])
            
            self.sortedImgHistory[self.curImageId] = {"currImgName": self.currImgName, "newImgName":  newImgName, "folderChosen": folderChosen, "date": self.currImgDate, "imageInHistory": imageInHistory}
            
            oldImageId = self.curImageId
            self.curImageId = self.curImageId + 1

            if self.curImageId < self.imageCount:
                self.gui.updateImageUI()
                if not OCR_AFTER and not self.willCloseWindows:
                    self.threadedOCR(oldImageId, self.inOCRSet)
                self.threadedListening()
                
            elif self.curImageId == self.imageCount:
                self.deactivateListeningPermanently = True
                self.toggleListening()
                self.gui.highlightChosenFolder()
                
                if not OCR_AFTER and not self.willCloseWindows:
                    self.unthreadedOCR(oldImageId, self.inOCRSet)
                else:
                    self.runOCR(self.folderPath)
                    if not self.willCloseWindows:
                        self.dialog.dialogFinalImage()
                self.willCloseWindows = True
                self.willCloseThread = True

        
    def imageActionTextFade(self):
        def reset():
            self.imageActionText.setText("")
        timer1 = QTimer(self)
        timer1.timeout.connect(reset)
        timer1.start(1000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.aboutToQuit.connect(ex.closeEvent)
    sys.exit(app.exec_())
