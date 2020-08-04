import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import shutil
import os, time, threading, math
from enum import Enum
import speech_recognition as sr
import traceback
from components.CustomWidgets import TimerMessageBox, WorkerSignals, Worker, Label, Canvas
from components.Dialog import Dialog
from components.Gui import Gui 
from components.helpers import boldenFont, getTime

try:
    from PIL import Image
except ImportError:
    import Image

from _constants import * 

def out(str):
    if CONSOLE:
        print(str)