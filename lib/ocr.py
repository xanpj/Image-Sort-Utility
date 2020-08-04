import sys
sys.path.append("..") # Adds higher directory to python modules path.
from _imports import *

import pytesseract

#for release bundling
if not DEV:
    def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    tesseractPath = resource_path('bin/tesseract')
    pytesseract.pytesseract.tesseract_cmd = tesseractPath

def threadedOCR(self, imgId, callback):
    try:
        worker = Worker(self.processOCR, imgId) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(callback)
        worker.signals.progress.connect(self.outShowProgressOCR)
        self.threadpool.start(worker) 
    except Exception as e:
       out("Error: unable to start thread")
       out(e)

def unthreadedOCR(self, arg, callback):
    return callback(self.processOCR(arg, callback))

def runOCR(self, path = None):
    self.threadpool.setMaxThreadCount(self.idealThreadCount)
    if self.dialog.dialogBinary(MSG['RUN_OCR_Q']):
        OCR_AFTER = True
        self.deactivateListeningPermanently = True
        self.toggleListening()

        if not path:
            dialogText = MSG["DIR_OCR"]
            self.dialog.dialogInfo(dialogText)
            self.ocrImagesPath = str(QFileDialog.getExistingDirectory(self, dialogText))
        else:
            self.ocrImagesPath = path

        def removeDS(p, folderNames):
            if DS_STORE in folderNames:
                folderNames.remove(DS_STORE)
            return folderNames

        def extractFiles(pf):
            files = os.listdir(pf)
            files = removeDS(pf, files)
            for file in files:
                img = pf+"/"+file
                if(os.path.isfile(img)):
                    self.imageArrOCR.append(img)

        p = self.ocrImagesPath
        try:
            folderNames = os.listdir(p)
            folderNames = removeDS(p, folderNames)

            for folder in folderNames:
                out(folder)
                pf = p+"/"+folder
                if os.path.isdir(pf): #one level only
                    extractFiles(pf)
                else:
                    extractFiles(p)
                    break;

        except Exception as e:
                out("Directory error when running OCR")
                out(e)

        imageCount = len(self.imageArrOCR)
        for i in range(imageCount):
            out("thread: " + str(i))
            self.threadedOCR(i, self.outOCRSave)

        text = MSG["RUNNING_OCR"]
        bgText = MSG["RUNNING_OCR"]
        self.messageBox = TimerMessageBox(self, None, text, bgText, imageCount)
        self.messageBox.exec_()

    
''' COMMON '''
def processOCR(self, imgId, progressCallback):
    imgPath = ""
    if not OCR_AFTER:
        curr = self.sortedImgHistory[imgId]
        imgPath = self.folderPath + "/" + curr["folderChosen"] + "/" + curr["newImgName"]
    else: 
        imgPath = self.imageArrOCR[imgId]
    ocrText = ""
    try:
        ocrText = pytesseract.image_to_string(Image.open(imgPath), lang=OCR_LANG) #lang='eng'
    except Exception as e:
        out("Error: OCR failed." + str(e))
    finally:
        if OCR_AFTER:
            progressCallback.emit(imgId)
    return [imgId, imgPath, ocrText]

''' Run OCR (OUT OF PROCESS) '''

def outFinishOCR(self, imgCount):
    self.outOCRWrite()
    self.messageBox.done(1) 
    self.dialog.dialogFinalImage(MSG["OCR_FINISHED"].format(str(imgCount)))

def outShowProgressOCR(self, i):
    imgCount = len(self.imageArrOCR)

    self.messageBox.updateProgress()
    out("Progress" + str(i+1) + "/" + str(imgCount))
    if(i == imgCount - 1):
        def checkData():
            if(len(self.imageArrOCRData) == imgCount):
                self.outFinishOCR(imgCount)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(checkData)
        self.timer.start()



def outOCRSave(self, result):
    [imgId, imgPath, imgText] = result
    try:
        imgData = {"file": imgPath, "ocr":  imgText, "date": getTime(imgPath)}
    except Exception as e:
        imgData = {"file": imgPath, "ocr":  imgText, "date": ""}
    self.imageArrOCRData[imgId] = imgData
    out(self.imageArrOCRData[imgId]["file"])

def outOCRWrite(self):
    f = open(self.ocrImagesPath+"/"+IMAGE_TXT, mode='a', encoding='utf-8') #stays self.folderPath
    for i, imgData in self.imageArrOCRData.items():
        filePath = imgData.get("file")
        fileName = os.path.basename(os.path.normpath(filePath))

        #extracting last folder before file
        folderChosenPath = filePath[::-1].replace(fileName[::-1], "", 1)[::-1]
        folderChosen = os.path.basename(os.path.normpath(folderChosenPath))

        ocr = imgData.get("ocr")
        date = str(imgData.get("date"))
        f.write("--------------------"+LINE_BREAK)
        f.write("Date: " + date + LINE_BREAK) 
        f.write("File Name: " + fileName + LINE_BREAK)
        f.write("Category: " + folderChosen + LINE_BREAK) 
        f.write(LINE_BREAK)
        f.write(ocr + LINE_BREAK)
    f.close()

''' IN THE PROCESS '''

def inOCRSet(self, result):
    [imgId, imgPath, ocrText] = result
    curr = self.sortedImgHistory[imgId]
    if curr is not None:
        self.inOCRWrite(curr, ocrText)

def inOCRWrite(self, curr, ocrText):
    out("WriteImageOCR")
    f = open(self.folderPath+"/"+IMAGE_TXT, 'a') #stays self.folderPath
    fileMovedSign = '*' if curr["imageInHistory"] else ''
    f.write("--------------------"+LINE_BREAK)
    f.write("Date: " + str(curr["date"]) + LINE_BREAK) 
    f.write("File Name: " + curr["newImgName"] + LINE_BREAK)
    f.write("Category: " + curr["folderChosen"] + LINE_BREAK)
    f.write("Original File Name: " + curr["currImgName"] + LINE_BREAK)
    f.write(fileMovedSign+"File renamed or moved: " + str(curr["imageInHistory"]) + LINE_BREAK)
    f.write(LINE_BREAK)
    f.write(ocrText + LINE_BREAK)
    f.close()
