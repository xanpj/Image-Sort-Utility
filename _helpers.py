from PyQt5.QtGui import *
import os, time

def boldenFont(widget, bold=True, unSelectList=None, unSelectListLength=0):
    if unSelectList is not None:
    	for i in range(0, unSelectListLength):
    		myFontRegular = QFont()
    		myFontRegular.setBold(False)
    		sender = unSelectList.itemAt(i).widget()
    		sender.setFont(myFontRegular)
    myFontBold = QFont()
    myFontBold.setBold(bold)
    widget.setFont(myFontBold)

def getTime(file):
	return time.strftime("%b %d %Y %H:%M:%S", time.gmtime(os.path.getmtime(file)))
