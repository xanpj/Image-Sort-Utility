import sys
sys.path.append("..") # Adds higher directory to python modules path.
from _imports import *
from _constants import *
from _helpers import boldenFont

class Dialog:
    def __init__(self, parent=None):
        self.parent = parent

    def setDialogInfoAbout(self, text):
        self.about = text

    def dialogInfoAbout(self):
        self.dialogInfo(self.about)

    def setDialogInfoUsage(self, text):
        self.folderName = text

    def dialogInfoUsage(self):
        MSG["INFO_USAGE_PT2"][2] = MSG["INFO_USAGE_PT2"][2].format(self.folderName)
        self.dialogInfo(MSG["INFO_USAGE_PT1"], MSG["INFO_USAGE_PT2"])
          #"3) Text inside the images can be found in "+self.folderName+"/images_file.txt",
          # "*When checking images_text.txt, beware that some images might have been renamed or recategorized.",
    
    def dialogInfo(self, text, furtherText=[], button=True):
       d = QDialog(self.parent)

       l0 = QLabel(text, d)
       l0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       l0.setAlignment(Qt.AlignCenter)
       l0.setFixedSize(l0.fontMetrics().boundingRect(l0.text()).width()+40, 20)

       buttonOffset = 50
       vbox = QVBoxLayout()

       if len(furtherText) == 0:
            vbox.addWidget(l0, alignment=Qt.AlignCenter)
       l0_added = False
       lineCounter = 0

       l = [None] * len(furtherText)
       for line in furtherText:
            if not l0_added:
                vbox.addWidget(l0, alignment=Qt.AlignLeft)
                l0_added = True

            l[lineCounter] = QLabel(line)
            l[lineCounter].setFixedSize(l[lineCounter].fontMetrics().boundingRect(l[lineCounter].text()).width()+40, 20)
            l[lineCounter].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            l[lineCounter].setAlignment(Qt.AlignCenter)
            l[lineCounter].move(0, 30)

            vbox.addWidget(l[lineCounter], alignment=Qt.AlignLeft)
            buttonOffset+=30
            lineCounter += 1

       if button:
            b1 = QPushButton(MSG["CLOSE"])
            vbox.addWidget(b1, alignment=Qt.AlignCenter)
            b1.clicked.connect(d.close)
            b1.move(70, buttonOffset)
            b1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

       d.setLayout(vbox)
       d.setWindowTitle(MSG["DIALOG_INSTR"])
       d.setWindowModality(Qt.ApplicationModal)
       d.setAttribute(Qt.WA_DeleteOnClose)
       d.exec_()

    def dialogFinalImage(self, text = MSG["ALL_PROCESSED"]):
        d = QDialog(self.parent)

        b0 = QLabel(text)
        b1 = QPushButton(MSG["CLOSE"])
        b0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        b0.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(b0, alignment=Qt.AlignCenter)
        vbox.addWidget(b1, alignment=Qt.AlignCenter)
        d.setLayout(vbox)

        b1.clicked.connect(d.close)
        b1.clicked.connect(self.parent.close)

        d.setWindowTitle(MSG["FINISHED"])
        d.setWindowModality(Qt.ApplicationModal)
        self.parent.willCloseWindows = False
        d.setAttribute(Qt.WA_DeleteOnClose)
        d.exec_()

    def dialogBinary(self, text):
      qm = QMessageBox(self.parent)
      ret = qm.question(self.parent,'', text, qm.Yes | qm.No)
      qm.close()
      return ret == qm.Yes