import sys
sys.path.append("..") # Adds higher directory to python modules path.
from _imports import *
from _constants import *
from _helpers import boldenFont


class TimerMessageBox(QMessageBox):
    def __init__(self, parent=None, timeout=3, text="", bgText="", maxProgress = 0):
        super(TimerMessageBox, self).__init__(parent)
        self.time_to_wait = timeout
        self.progress = 0
        self.maxProgress = maxProgress
        self.setWindowTitle(bgText)
        self.setText(text);
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QTimer(self)
        if timeout is not None:
            self.setInformativeText(MSG["WAIT_SECONDS"].format(self.time_to_wait))
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.changeContent)
            self.changeContent()
            self.timer.start()
        else:
            self.setInformativeText(MSG["PROGRESS"].format(self.progress, self.maxProgress));

    def updateProgress(self):
        self.progress += 1
        self.setInformativeText(MSG["PROGRESS"].format(self.progress, self.maxProgress));

    def changeContent(self):
        self.setInformativeText(MSG["WAIT_SECONDS"].format(self.time_to_wait))
        if self.time_to_wait <= 0:
            self.close()
        self.time_to_wait -= 1

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


class Label(QLabel):
    clicked=pyqtSignal()
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def enterEvent(self, event):
        boldenFont(self, True)

    def leaveEvent(self, event):
        boldenFont(self, False)

class Canvas(Label):
    def __init__(self, parent=None, imageWidth=500, imageHeight=500):
        QLabel.__init__(self, parent)
        self.parent = parent
        self.clickActivated = False
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight
        self.pen = QPen(QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QBrush(QColor(255,255,255,255))        # set fillColor  
        self.brush1 = QBrush(QColor(255,255,255,128))        # set fillColor  
        self.polygon = self.createPoly(3,100,0,self.imageWidth)

    def mousePressEvent(self, ev):
        self.clickActivated = not self.clickActivated
        self.clicked.emit()
        self.update()

    def createPoly(self, n, r, s, left_offset):
        polygon = QPolygonF() 
        w = 360/n                                                       # angle per step
        for i in range(n):                                              # add the points of polygon
            t = w*i + s
            x = r*math.cos(math.radians(t))
            y = r*math.sin(math.radians(t))
            polygon.append(QPointF(self.imageWidth/2 + x,  self.parent.height/2 + y - r/2))
        return polygon

    def paintEvent(self, event):
        QLabel.paintEvent(self, event)
        if self.clickActivated:
            painter = QPainter(self)
            painter.setBrush(self.brush1) 
            painter.drawRect(0, self.height()/2 - self.imageHeight/2, self.imageWidth-1, self.imageHeight) 
            painter.setPen(self.pen)
            painter.setBrush(self.brush) 
            painter.drawPolygon(self.polygon)


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        self.kwargs['progressCallback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        result = False
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if(result != False): #if main thread not ended
                self.signals.result.emit(result)  # Return the result of the processing
        finally:
            if(result != False): #if main thread not ended
                self.signals.finished.emit()  # Done



