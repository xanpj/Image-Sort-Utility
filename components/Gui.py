import sys
sys.path.append("..") # Adds higher directory to python modules path.
from _imports import *
from _constants import *
from _helpers import boldenFont

class Gui:
    def __init__(self, parent=None, imageWidth=500):
        self.parent = parent
        self.imageWidth = imageWidth #overwritten immediately on resize

        self.parent.setGeometry(0, 0, self.parent.width, self.parent.height)
        self.center()

    def initUI(self):
        self.parent.setWindowTitle(self.parent.title)

        self.parent.folderNames = self.renderFolderList()
        self.parent.imageActionText = QLabel(self.parent)
        #boldenFont(self.parent.imageSortedTo)

        self.parent.lineEdit = QLineEdit(self.parent)
        self.parent.lineEdit.setVisible(False)
        self.parent.lineEdit.returnPressed.connect(self.parent.returnPressed)
    
    def center(self):
        cp = QDesktopWidget().availableGeometry().center()
        qr = self.parent.frameGeometry()
        qr.moveCenter(cp)
        self.parent.move(qr.topLeft())

    def createWindowMenuAndFooter(self):
        menu = self.parent.menuBar()

        mainMenu = menu.addMenu('&Menu')
        ocrMenuAction = QAction('Run OCR', self.parent)
        usageMenuAction = QAction('Usage', self.parent)
        infoMenuAction = QAction('Info', self.parent)
        mainMenu.addAction(ocrMenuAction)
        mainMenu.addAction(usageMenuAction)
        mainMenu.addAction(infoMenuAction)
        
        ocrMenuAction.triggered.connect(self.parent.runOCR)
        usageMenuAction.triggered.connect(self.parent.dialog.dialogInfoUsage)
        infoMenuAction.triggered.connect(self.parent.dialog.dialogInfoAbout)

        self.parent.statusbar = self.parent.statusBar()

    def renderFolderList(self):
        self.parent.folderNameList = []
        foldervbox = QVBoxLayout()

        folderNames = os.listdir(self.parent.folderPath)
        try:
            folderNames.remove(DS_STORE)
        except:
            out("")
        folders = []
        for f in folderNames:
            folder = Label(self.parent)
            folder.setText(f)
            folder.clicked.connect(self.parent.nextImageManual)
            foldervbox.addWidget(folder)
            self.parent.folderNameList.append(f.strip())
        return foldervbox

    def updateImageUI(self, imageWidth=None):        
        if imageWidth is not None:
            self.imageWidth = imageWidth

        self.parent.lineEdit.setText("")
        self.parent.box = self.createImageUI()
        self.parent.lineEdit.setVisible(False)
        self.parent.box.insertWidget(0, self.parent.lineEdit)

        self.highlightChosenFolder()

        mainWidget = QWidget()
        mainWidget.setLayout(self.parent.box)
        self.parent.setCentralWidget(mainWidget) 
        self.parent.show()


    def highlightChosenFolder(self):
        recKey = self.parent.recognizedKeyword
        self.parent.statusbar.showMessage(recKey)
        #self.parent.imageActionText.setText(recKey)
        if recKey is not None:
            chosenFolderElement = self.parent.getChosenFolderElement(recKey)
            unSelectList = self.parent.folderNames
            unSelectListLength = len(self.parent.folderNameList)
            boldenFont(chosenFolderElement, True, unSelectList, unSelectListLength)

    def createImageUI(self):
        self.parent.getImageName()

        image = self.drawImage()
        imageName = QLabel(self.parent)
        imageProgress = "("+str(self.parent.curImageId+1)+"/"+str(self.parent.imageCount)+")"
        imageNameText = imageProgress + " " + self.parent.currImgName
        imageName.setText(imageNameText)
        imageDate = QLabel(self.parent)
        imageDate.setText(self.parent.currImgDate)

        box = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        vbox.addWidget(imageDate)
        vbox.addWidget(self.parent.imageActionText)
        vbox.addStretch()

        self.parent.folderNames.setParent(None)
        #set the folderChosen to bold when going back in images
        folderChosenOption = ""
        if(len(self.parent.sortedImgHistory) > self.parent.curImageId
         and self.parent.sortedImgHistory[self.parent.curImageId] != None):
            folderChosenOption = self.parent.sortedImgHistory[self.parent.curImageId]["folderChosen"]
        
        for i in reversed(range(self.parent.folderNames.count())):
            bBoldenFont = False
            folderOptionWidget = self.parent.folderNames.itemAt(i).widget()
            if(folderChosenOption != ""):
                if(folderOptionWidget.text() == folderChosenOption):
                    bBoldenFont = True
            boldenFont(folderOptionWidget, bBoldenFont)
        vbox.addLayout(self.parent.folderNames)

        hbox.addLayout(vbox)
        hbox.addStretch()
        hbox.addWidget(image)

        box.addWidget(imageName)
        box.addLayout(hbox)

        return box

    def drawImage(self):
        try:
            pixmap = QPixmap(self.parent.currImg)
            resizedPixmap = pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio, Qt.FastTransformation)
            image = Canvas(self.parent, self.imageWidth, resizedPixmap.height() ) #load image as pixmap in label
            image.setPixmap(resizedPixmap)

            #self.parent.resize(resizedPixmap.width(),resizedPixmap.height())
            image.clicked.connect(self.parent.toggleListening)

            return image
        except Exception as e:
            out(e)
            self.parent.dialog.dialogInfo(MSG["INVALID_FOLDERS"])



