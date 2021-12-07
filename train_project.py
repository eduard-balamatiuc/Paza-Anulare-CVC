import cv2
import numpy as np
from numpy.lib.function_base import angle, percentile
import PoseModule as pm



class Train():
    def __init__(self):
        self.detector = pm.poseDetector()
        self.count = 0
        self.dir = 0 
        self.per = None

    def activate(self,img,exNameStr):
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        if len(lmList) != 0:
            if exNameStr == 'dips':
                self.per = self.detector.dips(img) 
            if exNameStr == 'biceps':
                self.per = self.detector.biceps_curls(img)
            if exNameStr == 'squats':
                self.per = self.detector.squats(img)
            if exNameStr == 'crunches':
                self.per = self.detector.crunches(img)    

            #check for the curls
            if self.per == 100:
                if self.dir == 0:
                    self.count += 0.5
                    self.dir = 1
            if self.per == 0:
                if self.dir == 1:
                    self.count += 0.5
                    self.dir = 0

            y_dimension, x_dimension = img.shape[:-1]

            cv2.rectangle(img, (0, y_dimension-90), (90, y_dimension), (61, 133, 255), cv2.FILLED)
            
            cv2.putText(img, str(int(self.count)), (20, y_dimension-20), cv2.FONT_HERSHEY_PLAIN, 5, (34, 34, 255), 5) 
        return img 