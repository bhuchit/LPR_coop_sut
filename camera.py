from threading import Thread, Lock
import cv2
import imutils
import argparse
from fps import FPS
class WebcamVideoStream(object):
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        
        self.started = False
        self.read_lock = Lock()

    def start(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()

        return self
    
    def update(self):
        while self.started:
            (self.grabbed, self.frame) = self.stream.read()
            self.read_lock.acquire()
            self.read_lock.release()
    
    def read(self):
        self.read_lock.acquire()
        self.read_lock.release()
        return self.frame
    
    def stop(self):
        self.started = False
        # self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()
        
