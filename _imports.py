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

from _helpers import boldenFont, getTime
from _constants import * 

try:
    from PIL import Image
except ImportError:
    import Image


def out(str):
    if CONSOLE:
        print(str)
