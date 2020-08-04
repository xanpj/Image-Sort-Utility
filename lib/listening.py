import sys
sys.path.append("..") # Adds higher directory to python modules path.
from _imports import *

r = sr.Recognizer()

def adjustForAmbientNoise(self):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2.0) # #  analyze the audio source

def toggleListening(self):
    if self.deactivateListeningPermanently:
        self.isListening = False

    if self.isListening:
        self.isListening = False
        self.statusbar.showMessage(MSG["PAUSED"])
        self.eventStop.set()
    else:
        if not self.deactivateListeningPermanently:
            self.isListening = True
            self.eventStop.clear()
            self.threadedListening()
            self.statusbar.showMessage(MSG["LISTENING"])    
        else:
            self.statusbar.showMessage("")    

def threadedListening(self):
    try:
        worker = Worker(self.listen, self.folderNameList) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.idle)
        worker.signals.finished.connect(self.closeThread)
        worker.signals.progress.connect(self.listeningProgress)
        self.threadpool.start(worker) 
    except Exception as e:
       out("Error: unable to start thread")
       out(e)

''' Main listening loop '''
def listen(self, folderNameList, progressCallback):
    recognizedKeyword = ""

    while(recognizedKeyword == "" and not self.eventStop.is_set() and self.isListening):
        with sr.Microphone() as source:
            out("Say something!")
            
            progressCallback.emit(0)
            audioDetected = False
            audio = None
            while(audioDetected is False and not self.eventStop.is_set() and self.isListening):
                try:
                    audio = r.listen(source, timeout=TIMEOUT) #
                    out("Audio detected")
                    audioDetected = True
                except sr.WaitTimeoutError as e:
                    out(e)
        if(audioDetected and not self.eventStop.is_set() and self.isListening):
            try:
                keywords = [(f, THRESHHOLD) for f in folderNameList]
                recognizedKeyword = r.recognize_sphinx(audio, keyword_entries=keywords).strip()
                out("Sphinx assumes you said " + recognizedKeyword)

                if(recognizedKeyword in folderNameList):
                    self.recognizedKeyword = recognizedKeyword
                    progressCallback.emit(1)
                    return recognizedKeyword
                else:
                    recognizedKeyword = ""
                    raise sr.UnknownValueError
            except sr.UnknownValueError:
                out("Sphinx could not understand audio")
                progressCallback.emit(2)
            except sr.RequestError as e:
                out("Sphinx error; {0}".format(e))
                progressCallback.emit(3)
        else:
            return False

def idle(self):
	out("idle")
